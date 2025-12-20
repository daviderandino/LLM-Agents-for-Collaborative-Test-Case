import os
import sys
import subprocess
import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

from src.utils.file_manager import obtain_import_module_str, read_text
from src.utils.code_parser import clean_llm_python, syntax_check
from src.utils.pytest_runner import run_pytest


# === DEFINIZIONE DELLO STATO DEL GRAFO ===
class AgentState(TypedDict):
    project_root: str
    input_file_path: str      # path del file .py per cui generare i test
    target_module: str        # nome del modulo per l'import (es: data.input_code.bank)
    code_under_test: str      # contenuto del file .py che dobbiamo testare
    
    test_plan: str            # il piano generato (to-do list) dal nodo planner
    generated_tests: str      # il codice pytest generato dal nodo generator
    
    error: str
    failed_tests_infos: str   # elenco di test failati nel formato 'FAILED nome_test - errore' (uno sotto l'altro)
    coverage_percent: int     # percentuale di coverage raggiunta con i test generati (0-100)
    n_passed_tests: int       # numero di test che passano
    n_failed_tests: int       # numero di test che failano

    iterations: int           # contatore per evitare loop infiniti tra gli agenti
    max_iterations: int       # numero massimo di iterazioni prima di finire il processo


# AGGIUNGERE UN REASONER/REVIEWER che, anche dopo che i test generati hanno coverage massima
# e passano tutti, ragioni sui test generati ad esempio se l'LLM sta barando facendo asserzioni
# del tipo "assert True". Ha senso ??? 

class MultiAgentCollaborativeGraph:
    def __init__(self, project_root, rel_input_file_path, llm_planner, llm_generator):
        """
        Inizializza il grafo di nodi, ad ogni nodo si può associare un llm
        differente.
        """
        self.llm_planner = llm_planner
        self.llm_generator = llm_generator

        self.graph = self._build_graph()

        code = read_text(rel_input_file_path)

        self.initial_state = {
            "project_root": project_root,
            "input_file_path": rel_input_file_path,
            "target_module": obtain_import_module_str(rel_input_file_path),
            "code_under_test": code,

            "test_plan": '',
            "generated_tests": '',

            "error": '',
            "failed_tests_infos": '',
            "coverage_percent": 0,
            "n_passed_tests": 0,
            "n_failed_tests": 0,
            "iterations": 0,
            "max_iterations": 5
        }


    def _build_graph(self):
        """
        Configura e compila il grafo di LangGraph.
        """

        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self._plan_node)
        workflow.add_node("generator", self._generation_node)
        workflow.add_node("executor", self._execution_node)
        
        workflow.set_entry_point("planner")
        
        workflow.add_edge("planner", "generator") # arco planner -> generator
        workflow.add_edge("generator", "executor") # arco generator -> executor
        workflow.add_conditional_edges( # arco condizionale executor -> (planner, END)
            "executor",
            self._route_to,
            {
                "re-plan": "planner", # se router ritorna 're-plan', l'arco è executor -> planner
                "end": END # se router ritorna 'end', l'arco è executor -> END
            }
        )
        
        return workflow.compile()
        

    def _plan_node(self, state: AgentState):
        """
        Analizza il codice e crea un piano di test.
        Se arriva da un fallimento (retry), legge l'errore precedente.
        """
        print(f"\n--- STEP 1: PLANNING (Iteration {state['iterations'] + 1}) ---")
        
        # costruisco il contesto: è la prima volta che facciamo planning o dobbiamo
        # correggere errori/aumentare la coverage?
        context = ""
        if state["generated_tests"]:
            context = f"""
            WARNING: PREVIOUS TEST EXECUTION FAILED, HAD LOW COVERAGE or SOME TEST FAILED TO PASS.

            Current Plan:
            {state['test_plan']}

            Current Generated Tests:
            {state['generated_tests']}

            Current Coverage: {state['coverage_percent']}%
            
            Failed Tests:
            {state['failed_tests_infos']}
            
            Current Errors:
            {state['error']}

            INSTRUCTION: Refine the plan to specifically fix errors and failed tests.
            """

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a QA Lead. Analyze the code and create a detailed step-by-step testing plan."),
            (
                "human",
                """
                Code to test:
                {code}
                
                {context}
                
                Return ONLY the textual plan (a concise TODO list of scenarios to test).
                """
            )
        ])
        
        chain = prompt | self.llm_planner
        response = chain.invoke({
            "code": state["code_under_test"],
            "context": context
        })
        
        # si aggiornano questi campi dello stato
        return {
            "test_plan": response.content,
            "iterations": state["iterations"] + 1
        }
    

    def _generation_node(self, state: AgentState):
        """
        Scrive il codice Python dei test basandosi sul piano.
        """
        print("--- STEP 2: GENERATING TESTS ---")
        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a Python Testing Expert (pytest).
                Write a complete test suite based on the plan provided. You have to reach the
                highest test coverage possible for the provided code.
                
                CRITICAL RULES:
                1. **ALWAYS start the file with `import pytest`**. This is mandatory.
                2. Import the module exactly using: `from {target_module} import ...`
                3. Use standard `pytest` syntax (fixtures, raises, marks).
                4. Output ONLY raw python code inside backticks (```python ... ```).
                5. Do NOT include explanations.
                6. Just output the code block, nothing else.
                7. **NO TEXT AFTER THE CODE**. Do not write "Here is the code" or "This covers X".
                """
            ),
            (
                "human",
                """
                Plan:
                {plan}
                
                Code to be tested:
                {code}
                
                Generate the full test file content.
                """
            )
        ])
        
        chain = prompt | self.llm_generator
        response = chain.invoke({
            "target_module": state["target_module"],
            "plan": state["test_plan"],
            "code": state["code_under_test"]
        })
        
        cleaned_code = clean_llm_python(response.content)
        
        return {
            "generated_tests": cleaned_code
        }


    def _execution_node(self, state: AgentState):
        """
        Salva il file, esegue pytest e ne processa l'output.
        """
        print("--- STEP 3: EXECUTING PYTEST ---")
        
        ok, err = syntax_check(state["generated_tests"])

        if not ok:
            print(f"--- EXECUTION RESULT: Syntax Error ---")
            return {
                "error": err,
                "failed_tests_infos": '',
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0,
            }

        test_results = run_pytest(state["target_module"], state["generated_tests"])
        
        print(f"--- EXECUTION RESULT: Coverage={coverage}% ---")
         

        return {
            "test_output": output,
            "coverage_percent": coverage,
            "error_occurred": is_error
        }
    

    def _route_to(self, state: AgentState):
        """
        Funzione decisionale che determina se dopo l'esecuzione
        dei test generati possiamo chiudere il processo oppure o
        tornare in planning.
        """
        
        max_iterations = state['max_iterations']

        if state["iterations"] >= max_iterations:
            print(f"--- STOPPING: Reached Max Iterations ({max_iterations}) ---")
            return "end"
        
        # Se i test passano (no errori) e la coverage è 100%, l'agente termina
        if not state["error_occurred"] and state["coverage_percent"] == 100:
            print("--- SUCCESS: 100% Coverage & Pass rate ---")
            return "end"
        
        # altrimenti, si rigenera il piano
        print("--- DECISION: Re-planning (Low coverage or Errors) ---")
        return "re-plan"


    def invoke(self):
        final_state = self.graph.invoke(self.initial_state)

        output_filename = f"test_{os.path.basename(input_file_rel)}"
        output_path = os.path.join(project_root, "data/output_tests", output_filename)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write(final_state["generated_tests"])