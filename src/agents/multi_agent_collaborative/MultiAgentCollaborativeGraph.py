import os
import sys
import subprocess
import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

from src.utils.file_manager import obtain_import_module_str, read_text
from src.utils.code_parser import clean_llm_python

# === DEFINIZIONE DELLO STATO DEL GRAFO ===
class AgentState(TypedDict):
    project_root: str
    input_file_path: str      # path del file .py per cui generare i test
    target_module: str        # nome del modulo per l'import (es: data.input_code.bank)
    code_under_test: str      # contenuto del file .py che dobbiamo testare
    
    test_plan: str            # il piano generato (to-do list) dal nodo planner
    generated_tests: str      # il codice pytest generato dal nodo generator
    
    test_output: str          # output della console di pytest a seguito dell'esecuzione dei test generati
    coverage_percent: int     # percentuale di coverage raggiunta con i test generati (0-100)
    error_occurred: bool      # flag: ci sono stati errori di sintassi/runtime?
    
    iterations: int           # contatore per evitare loop infiniti tra gli agenti
    max_iterations: int


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
            "test_output": '',
            "coverage_percent": 0,
            "error_occurred": False,
            "iterations": 0,
            "max_iterations": 5
        }


    def _build_graph(self):
        """
        Configura e compila il grafo di LangGraph.
        """

        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self.plan_node)
        workflow.add_node("generator", self.generation_node)
        workflow.add_node("executor", self.execution_node)
        
        workflow.set_entry_point("planner")
        
        workflow.add_edge("planner", "generator") # arco planner -> generator
        workflow.add_edge("generator", "executor") # arco generator -> executor
        workflow.add_conditional_edges( # arco condizionale executor -> (planner, END)
            "executor",
            self.route_to,
            {
                "re-plan": "planner", # se router ritorna 're-plan', l'arco è executor -> planner
                "end": END # se router ritorna 'end', l'arco è executor -> END
            }
        )
        
        return workflow.compile()
        

    def plan_node(self, state: AgentState):
        """
        Analizza il codice e crea un piano di test.
        Se arriva da un fallimento (retry), legge l'errore precedente.
        """
        print(f"\n--- STEP 1: PLANNING (Iteration {state['iterations'] + 1}) ---")
        
        # costruisco il contesto: è la prima volta che facciamo planning o dobbiamo
        # correggere errori/aumentare la coverage?
        context = ""
        if state.get("test_output"):
            context = f"""
            WARNING: PREVIOUS TEST EXECUTION FAILED or HAD LOW COVERAGE.
            Current Coverage: {state.get('coverage_percent', 0)}%
            
            Previous Output/Errors:
            {state['test_output']}
            
            INSTRUCTION: Refine the plan to specifically fix these errors and cover missing lines.
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
    

    def generation_node(self, state: AgentState):
        """
        Scrive il codice Python dei test basandosi sul piano.
        """
        print("--- STEP 2: GENERATING TESTS ---")
        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a Python Testing Expert (pytest).
                Write a complete test suite based on the plan provided.
                
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
                
                Original Code:
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


    def execution_node(self, state: AgentState):
        """
        Salva il file, esegue pytest e legge la coverage.
        """
        print("--- STEP 3: EXECUTING PYTEST ---")
        
        # Salvo il file di test temporaneo
        # Nota: Lo salvo nella root per semplicità di import
        test_filename = "temp_test_execution.py"
        test_file_path = os.path.join(state.get('project_root'), test_filename)
        
        with open(test_file_path, "w") as f:
            f.write(state["generated_tests"])
        
        # Eseguo Pytest
        cmd = [
            "pytest", 
            test_filename, 
            f"--cov={state['target_module']}",
            "--cov-report=term-missing"
        ]
        
        try:
            print(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=project_root, 
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            # Se il returncode non è 0, pytest ha fallito (test rossi o errore sintassi)
            is_error = result.returncode != 0

            # --- DEBUG PRINT ---
            if is_error:
                print("\n!!! PYTEST FAILURE OUTPUT !!!")
                print('\n'.join(output.splitlines()[-15:]))
                print("!!! END FAILURE OUTPUT !!!\n")

        except Exception as e:
            output = str(e)
            is_error = True
            print(f"EXCEPTION DURING EXECUTION: {e}")

        #parsing della Coverage
        cov_match = re.search(r"TOTAL.*?(\d+)%", output)
        coverage = int(cov_match.group(1)) if cov_match else 0
        
        print(f"--- EXECUTION RESULT: Errors={is_error}, Coverage={coverage}% ---")
        
        # rimuovo il file temporaneo se vuoi pulizia
        if os.path.exists(test_file_path):
            os.remove(test_file_path) 

        return {
            "test_output": output,
            "coverage_percent": coverage,
            "error_occurred": is_error
        }
    

    def route_to(self, state: AgentState):
        """
        Funzione decisionale che determina se dopo l'esecuzione
        dei test generati possiamo chiudere il processo oppure o
        tornare in planning.
        """
        
        max_iterations = state.get('max_iterations', 20)

        if state["iterations"] >= max_iterations:
            print(f"--- STOPPING: Reached max iterations ({max_iterations}) ---")
            return "end"
        
        # Se i test passano (no errori) e la coverage è 100%, l'agente termina
        if not state["error_occurred"] and state["coverage_percent"] == 100:
            print("--- SUCCESS: 100% Coverage achieved! ---")
            return "end"
        
        # altrimenti, si rigenera il piano
        print("--- DECISION: Re-planning (Low coverage or Errors) ---")
        return "re-plan"
