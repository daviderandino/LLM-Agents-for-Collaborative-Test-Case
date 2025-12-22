from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

from src.utils.file_manager import obtain_import_module_str, read_text
from src.utils.code_parser import clean_llm_python, syntax_check
from src.utils.pytest_runner import run_pytest


# Simple ANSI color helper for terminal prints
_ANSI_COLORS = {
    "reset": "\033[0m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "bold": "\033[1m",
}


def color_text(text: str, color: str = "reset") -> str:
    code = _ANSI_COLORS.get(color, "")
    reset = _ANSI_COLORS["reset"]
    return f"{code}{text}{reset}"


# === DEFINIZIONE DELLO STATO DEL GRAFO ===
class AgentState(TypedDict):
    input_file_path: str  # path del file .py per cui generare i test (è relativo alla root del progetto, dato che gli esperimenti partono da lì)
    target_module: str  # nome del modulo per l'import (es: data.input_code.bank_account se ho data/input_code/bank_account.py)
    code_under_test: str  # contenuto del file .py che dobbiamo testare

    test_plan: str  # il piano generato (to-do list) dal nodo planner
    generated_tests: str  # il codice pytest generato dal nodo generator

    error: str  # errore d'esecuzione di pytest (sono quelli gravi, ad esempio crash, non i singoli errori dei test case che li fanno failare)
    syntax_error: bool
    pytest_error: bool
    failed_tests_infos: str  # elenco di test failati nel formato 'FAILED nome_test - errore' (uno sotto l'altro)
    coverage_percent: (
        int  # percentuale di coverage raggiunta con i test generati (0-100)
    )

    n_passed_tests: int  # numero di test generati che passano
    n_failed_tests: int  # numero di test generati che failano

    iterations: int  # contatore per evitare loop infiniti tra gli agenti
    max_iterations: int  # numero massimo di iterazioni prima di finire il processo


# AGGIUNGERE UN REASONER/REVIEWER che, anche dopo che i test generati hanno coverage massima
# e passano tutti, ragioni sui test generati ad esempio se l'LLM sta barando facendo asserzioni
# del tipo "assert True". Ha senso ??? 

class MultiAgentCollaborativeGraph:
    def __init__(self, input_file_path, llm_planner, llm_generator):
        """
        Inizializza il grafo di nodi, ad ogni nodo si può associare un llm
        differente.
        """
        self.llm_planner = llm_planner
        self.llm_generator = llm_generator

        self.graph = self._build_graph()

        code = read_text(input_file_path)

        self.initial_state = {
            "input_file_path": input_file_path,
            "target_module": obtain_import_module_str(input_file_path),
            "code_under_test": code,
            "test_plan": "",
            "generated_tests": "",
            "error": "",
            "syntax_error": False,
            "pytest_error": False,
            "failed_tests_infos": "",
            "coverage_percent": 0,
            "n_passed_tests": 0,
            "n_failed_tests": 0,

            "iterations": 0,
            "max_iterations": 3,
        }


    def _build_graph(self):
        """
        Configura e compila il grafo di LangGraph.
        """

        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self._plan_node)
        workflow.add_node("developer", self._generation_node)
        workflow.add_node("executor", self._execution_node)

        workflow.set_entry_point("planner")

        workflow.add_edge("planner", "developer")  # arco planner -> developer
        workflow.add_edge("developer", "executor")  # arco developer -> executor
        workflow.add_conditional_edges(  # arco condizionale executor -> (planner, END)
            "executor",
            self._route_to,
            {
                "fix-tests": "developer",  # ci sono dei test che falliscono
                "replan": "planner",  # la coverage è troppo bassa
                "end": END,  # se router ritorna 'end', l'arco è executor -> END
            },
        )

        return workflow.compile()
        

    def _plan_node(self, state: AgentState):
        """
        Nodo Planner Intelligente.
        - Se iterations == 0: Genera il piano base (Strategia: Full Scan).
        - Se iterations > 0: Genera casi addizionali per alzare la coverage (Strategia: Gap Filling).
        """
        current_iter = state["iterations"]
        messages = []
        invoke_args = {}  # Dizionario per gli argomenti dinamici

        # SCENARIO 1: PRIMA GENERAZIONE (Cold Start)
        if current_iter == 0:
            print(color_text(f"\n--- STEP 1.1: PLANNING FROM SCRATCH ---", "cyan"))

            messages = [
                (
                    "system",
                    "Role: Senior Python QA Engineer obsessed with 100% Code Coverage.\n"
                    "Task: Dissect the provided code and generate a surgical JSON test plan.\n\n"
                    "Strategy for Max Coverage:\n"
                    "1. Branch Analysis: Generate a test for every `if`, `elif`, `else` and loop entry/exit.\n"
                    "2. Boundary Values: Test MIN, MAX, MIN-1, MAX+1, ZERO, NONE.\n"
                    '3. Data Types: Test empty lists `[]`, empty strings `""`, and `None`.\n'
                    "4. Exceptions: Trigger every `raise` statement.\n\n"
                    "Output Format:\n"
                    "Return a strictly valid JSON array where each object contains:\n"
                    '- "id": Unique identifier.\n'
                    '- "rationale": Explanation of coverage (CRITICAL).\n'
                    '- "target": Class.method or function name.\n'
                    '- "input": Arguments dictionary.\n'
                    '- "expected": Expected value or Exception name.\n\n'
                    "Strict Rules:\n"
                    "1. Output ONLY valid JSON.\n"
                    "2. Start response with `[` and end with `]`.\n"
                    "3. No markdown blocks, no explanations.",
                ),
                # FEW-SHOT (Input Code -> Output JSON)
                (
                    "human",
                    "Analyze:\ndef div(a, b):\n    if b == 0: raise ValueError()\n    return a / b",
                ),
                (
                    "ai",
                    "[\n"
                    '  {{"id": "T1_OK", "target": "div", "input": {{"a": 10, "b": 2}}, "expected": 5.0, "rationale": "Happy path"}},\n'
                    '  {{"id": "T2_ERR", "target": "div", "input": {{"a": 5, "b": 0}}, "expected": "ValueError", "rationale": "Zero division catch"}}\n'
                    "]",
                ),
                # INPUT REALE: Solo il codice sorgente
                ("human", "Analyze the following Python code:\n{code}"),
            ]

            # Argomenti per Scenario 1
            invoke_args = {"code": state["code_under_test"]}

        # SCENARIO 2: RE-PLANNING (Gap Filling con Context)
        else:
            cov = state.get("coverage_percent", 0)
            print(
                color_text(
                    f"--- STEP 1.2: RE-PLANNING (Current Coverage: {cov}%) ---",
                    "yellow",
                )
            )

            messages = [
                (
                    "system",
                    "Role: Python Coverage Specialist.\n"
                    "Context: The previous test suite failed to achieve 100% coverage.\n"
                    "Objective: Analyze the Source Code AND the Existing Tests to find MISSED logical paths.\n"
                    "Task: Generate ONLY the new test cases needed to fill the gaps.\n\n"
                    "Strategy for Gap Filling:\n"
                    "1. Deep Analysis: Compare Source Code vs Existing Tests to spot skipped branches.\n"
                    "2. Complex Logic: Focus on compound conditions (AND/OR) and edge boundaries missed by current tests.\n"
                    "3. No Duplicates: Do NOT regenerate tests that already exist.\n\n"
                    "Output Format:\n"
                    "Return a strictly valid JSON array where each object contains:\n"
                    '- "id": Unique identifier (e.g., T_MISSING_1).\n'
                    '- "rationale": Specific explanation of the gap this test covers.\n'
                    '- "target": Class.method or function name.\n'
                    '- "input": Arguments dictionary.\n'
                    '- "expected": Expected value or Exception name.\n\n'
                    "Strict Rules:\n"
                    "1. Output ONLY valid JSON.\n"
                    "2. Start response with `[` and end with `]`.\n"
                    "3. No markdown blocks, no explanations.",
                ),
                # FEW-SHOT (Re-planning example)
                (
                    "human",
                    "Analyze code:\ndef check(x):\n    if x > 0 and x < 10:\n        return True\n    return False",
                ),
                (
                    "ai",
                    "[\n"
                    '  {{"id": "T_MISSING_EDGE", "target": "check", "input": {{"x": 10}}, "expected": false, "rationale": "Boundary value 10 was missed"}},\n'
                    '  {{"id": "T_MISSING_NEG", "target": "check", "input": {{"x": -1}}, "expected": false, "rationale": "Negative value path"}}\n'
                    "]",
                ),
                # INPUT REALE: Codice Sorgente + Test Esistenti
                (
                    "human",
                    "Previous coverage was insufficient ({current_cov}%).\n\n"
                    "SOURCE CODE:\n{code}\n\n"
                    "EXISTING TESTS (Do not regenerate these):\n{current_tests}\n\n"
                    "Identify the missing gaps and generate the JSON Plan for NEW tests only.",
                ),
            ]

            # Argomenti per Scenario 2 (Include generated_tests)
            invoke_args = {
                "code": state["code_under_test"],
                "current_tests": state["generated_tests"],
                "current_cov": cov,
            }

        # Costruzione e Invocazione
        prompt = ChatPromptTemplate.from_messages(messages=messages)
        chain = prompt | self.llm_planner

        # Usiamo invoke_args che è stato popolato dinamicamente
        response = chain.invoke(invoke_args)

        print(color_text(f"RESPONSE JSON: {response.content}", "magenta"))

        return {"test_plan": response.content}

    def _generation_node(self, state: AgentState):
        """
        Scrive il codice Python dei test basandosi sul piano generato dal planner.
        """
        print("--- STEP 2: GENERATING TESTS ---")
        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
"""
You are a Python Testing Expert (pytest).
Your goal is to write or modify a test suite to achieve 100% coverage and fix any existing errors.
                
**CRITICAL INSTRUCTIONS FOR TEST GENERATION**:
- ALWAYS start the file with `import pytest`. This is mandatory.
- Import the module exactly using: `from {target_module} import ...`.
- ALWAYS include all the necessary imports that appears in the code to be tested, at the top of the generated tests code.
- Use standard `pytest` syntax (fixtures, raises, marks).

**CRITICAL INSTRUCTIONS IF PREVIOUS TESTS ARE PROVIDED**:
- Analyze the previous tests if provided, do NOT rewrite the whole file from scratch unless necessary.
- Fix or delete and replace failing tests.

**OUTPUT FORMAT**:
- Output ONLY raw python code inside backticks (```python ... ```).
- Do NOT include explanations.
- NO TEXT AFTER THE CODE. Do not write "Here is the code" or "This covers X".
"""
            ),
            (
                "human",
"""
**Plan**:
{plan}

**Code to test**:
{code}
                
**Previous tests for the code**:
{tests}

Generate the full test file content in order to achieve the highest coverage possible.
"""
            )
        ])
        
        chain = prompt | self.llm_generator
        response = chain.invoke({
            "target_module": state["target_module"],
            "plan": state["test_plan"],
            "code": state["code_under_test"],
            "tests": state["generated_tests"] or 'None'
        })
        
        cleaned_tests = clean_llm_python(response.content)

        return {
            "generated_tests": cleaned_tests
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

        report = run_pytest(state["target_module"], state["generated_tests"])

        if report["crash"] == 'yes':
            print(f"--- EXECUTION RESULT: Pytest Crash ---")

            return {
                "error": report["error_summary"],
                "failed_tests_infos": '',
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0
            }
        
        print(f"--- EXECUTION RESULT: Coverage={report['coverage']}% {report['passed']} Passed {report['failed']} Failed ---")
        
        return {
            "error": '',
            "failed_tests_infos": report["failed_tests_infos"],
            "coverage_percent": report["coverage"],
            "n_passed_tests": report["passed"],
            "n_failed_tests": report["failed"]
        }
    

    def _route_to(self, state: AgentState):
        """
        Funzione decisionale che determina se dopo l'esecuzione
        dei test generati possiamo chiudere il processo oppure
        tornare in planning.
        """
        
        max_iterations = state['max_iterations']

        if state["iterations"] >= max_iterations:
            print(f"--- STOPPING: Reached Max Iterations ({max_iterations}) ---")
            return "end"
        
        if state["n_failed_tests"] == 0 and state["coverage_percent"] == 100:
            print(f"--- SUCCESS: Task Completed in {state['iterations']} iteration ---")
            return "end"
        
        # altrimenti, si rigenera il piano
        print("--- DECISION: Re-planning ---")
        return "re-plan"


    def invoke(self):
        final_state = self.graph.invoke(self.initial_state)

        output_filename = f"test_{Path(final_state['input_file_path']).stem}.py"
        output_file_path = Path("data") / "output_tests" / "multi_agent_collaborative" / output_filename
        
        with open(str(output_file_path), "w") as f:
            f.write(final_state["generated_tests"])

        return final_state