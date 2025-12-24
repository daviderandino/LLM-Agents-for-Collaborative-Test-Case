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
    generated_tests: str  # il codice pytest migliore tra i due developer ad ogni iterazione

    candidate_tests_1: str
    candidate_tests_2: str

    # report del vincitore
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


class MultiAgentCompetitiveGraph:
    def __init__(self, input_file_path, llm_planner, llm_generator_1, llm_generator_2, verbose = True):
        """
        Inizializza il grafo di nodi, ad ogni nodo si può associare un llm
        differente.
        """
        self.llm_planner = llm_planner
        self.llm_generator_1 = llm_generator_1
        self.llm_generator_2 = llm_generator_2
        self.verbose = verbose

        self.graph = self._build_graph()

        code = read_text(input_file_path)

        self.initial_state = {
            "input_file_path": input_file_path,
            "target_module": obtain_import_module_str(input_file_path),
            "code_under_test": code,
            "test_plan": "",
            "generated_tests": "",
            "candidate_tests_1": "",
            "candidate_tests_2": "",
            "error": "",
            "syntax_error": False,
            "pytest_error": False,
            "failed_tests_infos": "",
            "coverage_percent": 0,
            "n_passed_tests": 0,
            "n_failed_tests": 0,
            "iterations": 0,
            "max_iterations": 10,
        }

    def _build_graph(self):
        """
        Configura e compila il grafo di LangGraph.

        Planner -> (Dev1 // Dev2) -> Executor
        """

        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self._plan_node)
        workflow.add_node("developer_1", self._gen_wrapper_1)
        workflow.add_node("developer_2", self._gen_wrapper_2)
        workflow.add_node("executor", self._execution_node)

        workflow.set_entry_point("planner")

        workflow.add_edge("planner", "developer_1")
        workflow.add_edge("planner", "developer_2")
        workflow.add_edge("developer_1", "executor")
        workflow.add_edge("developer_2", "executor")
        workflow.add_conditional_edges(
            "executor",
            self._route_to
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
                (
                    "human",
                    "Analyze the following Python code:\n{code}"
                )
            ]

            # Argomenti per Scenario 1
            invoke_args = {"code": state["code_under_test"]}

            # Esecuzione Scenario 1
            prompt = ChatPromptTemplate.from_messages(messages=messages)
            chain = prompt | self.llm_planner
            response = chain.invoke(invoke_args)

            if self.verbose: 
                print(color_text(f"RESPONSE: {response.content}", "magenta"))
            
            # Ritorna direttamente il piano (è il primo)
            return {
                "test_plan": response.content
            }

        # SCENARIO 2: RE-PLANNING (Gap Filling con Context)
        else:
            cov = state.get("coverage_percent", 0)
            print(color_text(
                    f"--- STEP 1.2: RE-PLANNING (Current Coverage: {cov}%) ---",
                    "yellow"
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
                )
            ]

            # Argomenti per Scenario 2 (Include generated_tests)
            invoke_args = {
                "code": state["code_under_test"],
                "current_tests": state["generated_tests"],
                "current_cov": cov,
            }

            # Esecuzione Scenario 2
            prompt = ChatPromptTemplate.from_messages(messages=messages)
            chain = prompt | self.llm_planner
            response = chain.invoke(invoke_args)

            # --- LOGICA DI APPEND PURA (String Manipulation) ---
            new_plan_fragment = response.content.strip()
            
            # Pulizia di sicurezza: se l'LLM ha messo comunque le quadre (per abitudine), le togliamo
            if new_plan_fragment.startswith("["):
                new_plan_fragment = new_plan_fragment[1:]
            if new_plan_fragment.endswith("]"):
                new_plan_fragment = new_plan_fragment[:-1]
            
            new_plan_fragment = new_plan_fragment.strip()

            # Recuperiamo il piano precedente
            old_plan = state.get("test_plan", "[]").strip()
            
            # Togliamo la quadra di chiusura del vecchio piano ']'
            if old_plan.endswith("]"):
                old_plan_base = old_plan[:-1].strip()
            else:
                old_plan_base = old_plan # Caso edge, non dovrebbe capitare

            # Gestione della virgola: se il vecchio piano era vuoto "[]", old_plan_base è "[".
            # Non vogliamo "[ , {nuovo} ]", ma "[ {nuovo} ]".
            if old_plan_base == "[":
                updated_full_plan = old_plan_base + new_plan_fragment + "]"
            else:
                updated_full_plan = old_plan_base + ", " + new_plan_fragment + "]"

            if self.verbose:
                print(color_text(f"RESPONSE FRAGMENT: {new_plan_fragment}", "magenta"))

            return {
                "test_plan": updated_full_plan
            }

    def _gen_wrapper_1(self, state: AgentState):
        print(color_text("--- DEV 1 WORKING ---", "cyan"))
        result_code = self._generation_logic(state, self.llm_generator_1, "DEV 1")
        return {
            "candidate_tests_1": result_code
        }
    
    def _gen_wrapper_2(self, state: AgentState):
        print(color_text("--- DEV 2 WORKING ---", "cyan"))
        result_code = self._generation_logic(state, self.llm_generator_2, "DEV 2")
        return {
            "candidate_tests_2": result_code
        }

    def _generation_logic(self, state: AgentState, llm, agent_name: str):
        """
        Funzione helper usata da entrambi i Developer.
        """
        messages = []
        invoke_args = {}
        step_name = ""
        color = "white"
        is_append_mode = False

        iter_num = state["iterations"]
        n_failed = state["n_failed_tests"]
        syntax_err = state["syntax_error"]
        pytest_err = state["pytest_error"]
        base_code = state["generated_tests"]

        # ---------------------------------------------------------
        # 1. SELEZIONE STRATEGIA (Prompt Originali Intatti)
        # ---------------------------------------------------------

        # CASO 1: Prima iterazione (Generazione da zero)
        if iter_num == 0:
            step_name = f"--- STEP 2.1: {agent_name} GENERATING TESTS FROM SCRATCH---"
            color = "cyan"
            messages = [
                (
                    "system",
                    "Role: Senior Pytest Engineer."
                    "Task: Convert JSON Test Plan into a production-grade test suite."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source."
                    "- 2. Strategy: Group tests with `@pytest.mark.parametrize` where possible."
                    "- 3. Logic: If `expected` in JSON is an Exception name (e.g. 'ValueError'), use `with pytest.raises(...)`. Else use `assert result == expected`."
                    "- 4. Classes: If target is `Class.method`, instantiate the class first."
                    "- 5. Output: Start output with exactly: ```python, and end output with exactly: ```. No text.",
                ),
                (
                    "human",
                    "Plan: [{{'target': 'div', 'input': {{'a': 10, 'b': 2}}, 'expected': 5}}, {{'target': 'div', 'input': {{'a': 5, 'b': 0}}, 'expected': 'ZeroDivisionError'}}]\nCode: def div(a,b): return a/b",
                ),
                (
                    "ai",
                    "```python\nimport pytest\nfrom calc import div\n\n@pytest.mark.parametrize('a, b, expected', [\n    (10, 2, 5)\n])\ndef test_div_success(a, b, expected):\n    assert div(a, b) == expected\n\ndef test_div_error():\n    with pytest.raises(ZeroDivisionError):\n        div(5, 0)\n```",
                ),
                (
                    "human", 
                    "Plan: {plan}\nCode to test: {code}"
                )
            ]
            invoke_args = {
                "target_module": state["target_module"],
                "plan": state["test_plan"],
                "code": state["code_under_test"],
            }

        # CASO 2: I test girano ma falliscono (Assertion Errors)
        elif n_failed != 0:
            step_name = f"--- STEP 2.2: {agent_name} FIXING FAILED TESTS ---"
            color = "yellow"
            messages = [
                (
                    "system",
                    "Role: Senior Pytest Debugger."
                    "Task: Fix only the failing tests to achieve 100% pass rate."
                    "Strategy:"
                    "- 1. Analyze the Pytest failure report."
                    "- 2. Compare expectations vs actual Source Code behavior."
                    "- 3. ADJUST the test assertions/setup to match the Source Code reality."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source."
                    "- 2. Strategy: Group tests with `@pytest.mark.parametrize` where possible."
                    "- 3. Logic: If `expected` in JSON is an Exception name (e.g. 'ValueError'), use `with pytest.raises(...)`. Else use `assert result == expected`."
                    "- 4. Classes: If target is `Class.method`, instantiate the class first."
                    "- 5. Output: Start output with exactly: ```python, and end output with exactly: ```. No text.",
                ),
                (
                    "human",
                    "Source Code (Truth):{code}"
                    "Current Test Code:{previous_test_code}"
                    "Pytest Failure Report:{test_report}"
                    "Fix the assertions in the test code so they match the Source Code logic and PASS.",
                )
            ]
            invoke_args = {
                "code": state["code_under_test"],
                "target_module": state["target_module"],
                "previous_test_code": base_code,
                "test_report": state["failed_tests_infos"],
            }

        # CASO 3: Errore di Sintassi / Esecuzione
        # Nota: Ho mantenuto la logica "OR" sulle chiavi, usando .get per sicurezza
        elif syntax_err or pytest_err:
            step_name = "--- STEP 2.3: FIXING SYNTAX/PYTEST ERROR ---"
            color = "yellow"
            messages = [
                (
                    "system",
                    "Role: Python Code Fixer."
                    "Task: Fix the syntax/runtime error in the provided test file."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source."
                    "- 2. Strategy: Group tests with `@pytest.mark.parametrize` where possible."
                    "- 3. Logic: If `expected` in JSON is an Exception name (e.g. 'ValueError'), use `with pytest.raises(...)`. Else use `assert result == expected`."
                    "- 4. Classes: If target is `Class.method`, instantiate the class first."
                    "- 5. Output: Start output with exactly: ```python, and end output with exactly: ```. No text.",
                ),
                (
                    "human",
                    "The previous test code failed to execute.\nFAILED CODE: {previous_test_code}\nERROR TRACEBACK:{error}\nPlease provide the CORRECTED full test file code.",
                )
            ]
            invoke_args = {
                "previous_test_code": base_code,
                "target_module": state["target_module"],
                "error": state["error"],
            }

        # CASO 4: Aggiunta nuovi test (Expansion Mode)
        else:
            step_name = "--- STEP 2.4: APPENDING NEW TESTS ---"
            color = "cyan"
            is_append_mode = True
            messages = [
                (
                    "system",
                    "Role: Senior Pytest Engineer (Extension Mode)."
                    "Task: Write ONLY the NEW test functions defined in the JSON Plan to append to the existing suite."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source."
                    "- 2. Strategy: Group tests with `@pytest.mark.parametrize` where possible."
                    "- 3. Logic: If `expected` in JSON is an Exception name (e.g. 'ValueError'), use `with pytest.raises(...)`. Else use `assert result == expected`."
                    "- 4. Classes: If target is `Class.method`, instantiate the class first."
                    "- 5. Output: Start output with exactly: ```python, and end output with exactly: ```. No text.",
                ),
                (
                    "human",
                    "Source Code:\n{code}\n\nExisting Test Code:\n{previous_test_code}\n\nNew Test Plan (Cases to ADD):\n{plan}\n\nGenerate ONLY the python code for the NEW tests to be appended.",
                )
            ]
            invoke_args = {
                "target_module": state["target_module"],
                "plan": state["test_plan"],
                "code": state["code_under_test"],
                "previous_test_code": base_code
            }

        # ---------------------------------------------------------
        # 2. ESECUZIONE (Logica Unificata)
        # ---------------------------------------------------------
        print(color_text(step_name, color))

        prompt = ChatPromptTemplate.from_messages(messages=messages)
        chain = prompt | llm

        # Invoca l'LLM con gli argomenti specifici del caso selezionato
        response = chain.invoke(invoke_args)

        cleaned_tests = clean_llm_python(response.content)

        # ---------------------------------------------------------
        # 3. MERGE / UPDATE
        # ---------------------------------------------------------
        final_test_code = ""

        if is_append_mode:
            if self.verbose: print(color_text(f"APPENDING FRAGMENT:\n{cleaned_tests}", "magenta"))
            # Concatena: Vecchio + \n\n + Nuovo
            final_test_code = base_code + "\n\n" + cleaned_tests
        else:
            if self.verbose: print(color_text(f"GENERATED CODE:\n{cleaned_tests}", "magenta"))
            # Sovrascrive
            final_test_code = cleaned_tests

        return final_test_code

    def _execution_node(self, state: AgentState):
        """
        Esegue entrambi i codici candidati.
        Sceglie il migliore basandosi sulla Coverage.
        Aggiorna 'generated_tests' con il vincitore.
        """
        print(color_text("--- STEP 3: EXECUTING PYTEST & COMPARING CANDIDATES---", "cyan"))

        # Helper interno per eseguire un singolo test
        def evaluate_candidate(code_str):
            ok, err = syntax_check(code_str)
            if not ok:
                return {
                    "valid": False, "crash": False, "error": err, 
                    "coverage": 0, "passed": 0, "failed": 9999, "infos": ""
                }
            
            report = run_pytest(state["target_module"], code_str)
            if report["crash"] == "yes":
                return {
                    "valid": False, "crash": True, "error": report["error_summary"], 
                    "coverage": 0, "passed": 0, "failed": 9999, "infos": ""
                }
            
            return {
                "valid": True, "crash": False, "error": "",
                "coverage": report["coverage"],
                "passed": report["passed"],
                "failed": report["failed"],
                "infos": report["failed_tests_infos"]
            }
        
        # valutazione parallela (simulata sequenziale qui, ma concettualmente parallela)
        res1 = evaluate_candidate(state["candidate_tests_1"])
        res2 = evaluate_candidate(state["candidate_tests_2"])

        print(f"Dev 1 -> Valid: {res1['valid']}, Cov: {res1['coverage']}%, Fail: {res1['failed']}")
        print(f"Dev 2 -> Valid: {res2['valid']}, Cov: {res2['coverage']}%, Fail: {res2['failed']}")

        # si sceglie il test con la coverage più alta a prescindere dai test non-passati
        winner_code = ""
        winner_res = {}
        winner_name = ""

        # Priorità: Validità tecnica > Coverage > Minor numero di fallimenti
        
        # Se entrambi sono invalidi, prendo il primo (a caso, tanto fallirà nel routing)
        if not res1["valid"] and not res2["valid"]:
            winner_code = state["candidate_tests_1"]
            winner_res = res1
            winner_name = "None (Both Crashed)"
        
        # Se uno solo è valido, vince lui
        elif res1["valid"] and not res2["valid"]:
            winner_code = state["candidate_tests_1"]
            winner_res = res1
            winner_name = "Dev 1 (Dev 2 Crashed)"
        elif not res1["valid"] and res2["valid"]:
            winner_code = state["candidate_tests_2"]
            winner_res = res2
            winner_name = "Dev 2 (Dev 1 Crashed)"
            
        # Entrambi validi: confronto Coverage
        else:
            if res1["coverage"] > res2["coverage"]:
                winner_code = state["candidate_tests_1"]
                winner_res = res1
                winner_name = "Dev 1 (Better Coverage)"
            elif res2["coverage"] > res1["coverage"]:
                winner_code = state["candidate_tests_2"]
                winner_res = res2
                winner_name = "Dev 2 (Better Coverage)"
            else:
                # Coverage pari: guardiamo chi ha meno fail
                if res1["failed"] <= res2["failed"]:
                    winner_code = state["candidate_tests_1"]
                    winner_res = res1
                    winner_name = "Dev 1 (Tie-Break Failures)"
                else:
                    winner_code = state["candidate_tests_2"]
                    winner_res = res2
                    winner_name = "Dev 2 (Tie-Break Failures)"

        print(color_text(f"🏆 WINNER: {winner_name}", "green"))

        # update dello stato col vincitore
        return {
            "generated_tests": winner_code, # IL VINCITORE DIVENTA LA BASE
            "error": winner_res["error"],
            "syntax_error": not winner_res["valid"] and not winner_res["crash"],
            "pytest_error": winner_res["crash"],
            "failed_tests_infos": winner_res["infos"],
            "coverage_percent": winner_res["coverage"],
            "n_passed_tests": winner_res["passed"],
            "n_failed_tests": winner_res["failed"],
            "iterations": state["iterations"] + 1,
        }


    def _route_to(self, state: AgentState):
        """
        Funzione decisionale che determina se dopo l'esecuzione
        dei test generati possiamo chiudere il processo oppure
        tornare in planning o coding.
        """

        # 0. Safety Check: Uscita di emergenza per loop infiniti
        if state["iterations"] > state["max_iterations"]:
            return END

        # 1. PRIORITÀ AL FIX: Se c'è un errore tecnico (Crash) o logico (Fail)
        # DEVE tornare al GENERATOR per correggere il codice esistente.
        if (state["pytest_error"] or state["syntax_error"] or state["n_failed_tests"] > 0):
            return ["developer_1", "developer_2"]

        # 2. PRIORITÀ ALLA COVERAGE: Solo se i test passano (quindi error="" e failed=0)
        # controlliamo se abbiamo coperto tutto il codice.
        # Se la coverage è sotto la soglia (es. 100%), torniamo al PLANNER.
        current_cov = state.get("coverage_percent", 0)
        if current_cov < 100:
            return "planner"  # -> Vai a PLANNER

        # 3. SUCCESSO: Test passati e Coverage 100%
        return END

    def invoke(self):
        final_state = self.graph.invoke(self.initial_state)  # type: ignore

        output_filename = f"test_{Path(final_state['input_file_path']).stem}.py"
        output_file_path = (
            Path("data")
            / "output_tests"
            / "multi_agent_competitive"
            / output_filename
        )

        with open(str(output_file_path), "w") as f:
            f.write(final_state["generated_tests"])

        return final_state
