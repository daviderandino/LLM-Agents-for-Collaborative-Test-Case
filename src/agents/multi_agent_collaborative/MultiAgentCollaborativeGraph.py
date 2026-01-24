from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import logging

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


# === GRAPH STATE DEFINITION ===
class AgentState(TypedDict):
    input_file_path: str  
    target_module: str  
    code_under_test: str  

    test_plan: str  
    latest_plan_chunk: str 
    generated_tests: str  

    error: str  
    syntax_error: bool
    pytest_error: bool
    failed_tests_infos: str  
    coverage_percent: int

    n_passed_tests: int  
    n_failed_tests: int  

    iterations: int  
    max_iterations: int
    
    total_tokens: int 


class MultiAgentCollaborativeGraph:
    def __init__(self, input_file_path, output_dir, llm_planner, llm_generator, verbose = True, max_iterations=10):
        self.output_dir = output_dir
        self.llm_planner = llm_planner
        self.llm_generator = llm_generator
        self.verbose = verbose
        self.max_iterations = max_iterations
        self.logger = logging.getLogger("Agent")

        self.graph = self._build_graph()

        code = read_text(input_file_path)

        self.initial_state = {
            "input_file_path": input_file_path,
            "target_module": obtain_import_module_str(input_file_path),
            "code_under_test": code,
            "test_plan": "",
            "latest_plan_chunk": "", 
            "generated_tests": "",
            "error": "",
            "syntax_error": False,
            "pytest_error": False,
            "failed_tests_infos": "",
            "coverage_percent": 0,
            "n_passed_tests": 0,
            "n_failed_tests": 0,
            "iterations": 0,
            "max_iterations": self.max_iterations,
            "total_tokens": 0 
        }

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self._plan_node)
        workflow.add_node("developer", self._generation_node)
        workflow.add_node("executor", self._execution_node)

        workflow.set_entry_point("planner")

        workflow.add_edge("planner", "developer")  
        workflow.add_edge("developer", "executor")  
        workflow.add_conditional_edges(  
            "executor",
            self._route_to,
            {
                "fix-tests": "developer",  
                "replan": "planner",  
                "end": END,
            }
        )

        return workflow.compile()

    def _plan_node(self, state: AgentState):
        current_iter = state["iterations"]
        messages = []
        invoke_args = {}  

        # SCENARIO 1: FIRST GENERATION (Cold Start)
        if current_iter == 0:
            self.logger.info(color_text(f"\n--- STEP 1.1: PLANNING FROM SCRATCH ---", "cyan"))

            messages = [
                (
                    "system",
                    "Role: Senior Python QA Engineer.\n"
                    "Task: Dissect the provided code and generate a surgical JSON test plan.\n\n"
                    "Key Objective: Generate the minimum number of test cases necessary to achieve maximum code coverage.\n\n"
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
                # REAL INPUT: Just the source code
                (
                    "human",
                    "Analyze the following Python code:\n{code}"
                )
            ]

            invoke_args = {"code": state["code_under_test"]}

            prompt = ChatPromptTemplate.from_messages(messages=messages)
            chain = prompt | self.llm_planner
            response = chain.invoke(invoke_args)
            
            # Count Tokens
            tokens = response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
            current_tokens = state.get("total_tokens", 0)

            if self.verbose: 
                self.logger.debug(color_text(f"RESPONSE: {response.content}", "magenta"))
            return {
                "test_plan": response.content,
                "latest_plan_chunk": response.content,
                "total_tokens": current_tokens + tokens
            }

        # SCENARIO 2: RE-PLANNING (Gap Filling with Context)
        else:
            cov = state.get("coverage_percent", 0)
            self.logger.info(color_text(
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
                    "Task: Generate ONLY the new test cases needed to fill the gaps.\n"
                    "Key Constraint: Minimize test count while maximizing coverage - add only essential tests.\n\n"
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
                # FEW-SHOT 
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
                # INPUT REALE
                (
                    "human",
                    "Previous coverage was insufficient ({current_cov}%).\n\n"
                    "SOURCE CODE:\n{code}\n\n"
                    "EXISTING TESTS (Do not regenerate these):\n{current_tests}\n\n"
                    "Identify the missing gaps and generate the JSON Plan for NEW tests only.",
                )
            ]

            invoke_args = {
                "code": state["code_under_test"],
                "current_tests": state["generated_tests"],
                "current_cov": cov,
            }

            prompt = ChatPromptTemplate.from_messages(messages=messages)
            chain = prompt | self.llm_planner
            response = chain.invoke(invoke_args)
            
            # Count Tokens
            tokens = response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
            current_tokens = state.get("total_tokens", 0)

            # --- PURE APPEND LOGIC ---
            new_plan_fragment = response.content.strip()
            
            if new_plan_fragment.startswith("["):
                new_plan_fragment = new_plan_fragment[1:]
            if new_plan_fragment.endswith("]"):
                new_plan_fragment = new_plan_fragment[:-1]
            
            new_plan_fragment = new_plan_fragment.strip()

            old_plan = state.get("test_plan", "[]").strip()
            
            if old_plan.endswith("]"):
                old_plan_base = old_plan[:-1].strip()
            else:
                old_plan_base = old_plan 

            if old_plan_base == "[":
                updated_full_plan = old_plan_base + new_plan_fragment + "]"
            else:
                updated_full_plan = old_plan_base + ", " + new_plan_fragment + "]"

            if self.verbose:
                self.logger.debug(color_text(f"RESPONSE FRAGMENT: {new_plan_fragment}", "magenta"))

            return {
                "test_plan": updated_full_plan,
                "latest_plan_chunk": new_plan_fragment, # Pass ONLY the newly generated fragment
                "total_tokens": current_tokens + tokens
            }

    def _generation_node(self, state: AgentState):
        """
        Writes or fixes the Python code for the tests.
        """
        messages = []
        invoke_args = {}
        step_name = ""
        color = "white"
        is_append_mode = False

        # ---------------------------------------------------------
        # 1. STRATEGY SELECTION
        # ---------------------------------------------------------

        # CASE 1: First iteration
        if state["iterations"] == 0:
            step_name = "--- STEP 2.1: GENERATING TESTS FROM SCRATCH---"
            color = "cyan"
            messages = [
                (
                    "system",
                    "Role: Senior Pytest Engineer."
                    "Task: Convert JSON Test Plan into a production-grade test suite."
                    "Key Objectives:"
                    "- Generate the minimum number of test cases necessary to achieve maximum code coverage."
                    "- Ensure all test cases are correct and fully functional. Every test must pass."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source code. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the code to test."
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
                    "```python\nimport pytest\nfrom calc import *\n\n@pytest.mark.parametrize('a, b, expected', [\n    (10, 2, 5)\n])\ndef test_div_success(a, b, expected):\n    assert div(a, b) == expected\n\ndef test_div_error():\n    with pytest.raises(ZeroDivisionError):\n        div(5, 0)\n```",
                ),
                (
                    "human", 
                    "Plan: {plan}\nCode to test: {code}"
                )
            ]
            invoke_args = {
                "target_module": state["target_module"],
                "plan": state["latest_plan_chunk"],
                "code": state["code_under_test"],
            }

        # CASE 2: Tests run but fail
        elif state["n_failed_tests"] != 0:
            step_name = "--- STEP 2.2: FIXING FAILED TESTS ---"
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
                    "Key Objectives:"
                    "- Ensure all test cases are correct and fully functional. Every test must pass."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the source code."
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
                "previous_test_code": state["generated_tests"],
                "test_report": state["failed_tests_infos"],
            }

        # CASE 3: Syntax / Execution Error
        elif state.get("syntax_error") or state.get("pytest_error"):
            step_name = "--- STEP 2.3: FIXING SYNTAX/PYTEST ERROR ---"
            color = "yellow"
            messages = [
                (
                    "system",
                    "Role: Python Code Fixer."
                    "Task: Fix the syntax/runtime error in the provided test file."
                    "Key Objectives:"
                    "- Ensure all test cases are correct and fully functional. Every test must pass."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the source code."
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
                "previous_test_code": state["generated_tests"],
                "target_module": state["target_module"],
                "error": state["error"],
            }

        # CASE 4: Adding new tests (Expansion Mode)
        else:
            step_name = "--- STEP 2.4: APPENDING NEW TESTS ---"
            color = "cyan"
            is_append_mode = True
            messages = [
                (
                    "system",
                    "Role: Senior Pytest Engineer (Extension Mode)."
                    "Task: Write ONLY the NEW test functions defined in the JSON Plan to append to the existing suite."
                    "Key Objectives:"
                    "- Generate the minimum number of test cases necessary to achieve maximum code coverage."
                    "- Ensure all test cases are correct and fully functional. Every test must pass."
                    "Strict Rules:"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`.Import any other lib used in source. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the source code."
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
                "plan": state["latest_plan_chunk"],
                "code": state["code_under_test"],
                "previous_test_code": state["generated_tests"],
            }

        # ---------------------------------------------------------
        # 2. EXECUTION
        # ---------------------------------------------------------
        self.logger.info(color_text(step_name, color))

        prompt = ChatPromptTemplate.from_messages(messages=messages)
        chain = prompt | self.llm_generator

        # Invoke the LLM
        response = chain.invoke(invoke_args)
        
        # Count Tokens
        tokens = response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
        current_tokens = state.get("total_tokens", 0)

        cleaned_tests = clean_llm_python(response.content)

        # ---------------------------------------------------------
        # 3. MERGE / UPDATE
        # ---------------------------------------------------------
        final_test_code = ""

        if is_append_mode:
            if self.verbose: self.logger.debug(color_text(f"APPENDING FRAGMENT:\n{cleaned_tests}", "magenta"))
            final_test_code = state["generated_tests"] + "\n\n" + cleaned_tests
        else:
            if self.verbose: self.logger.debug(color_text(f"GENERATED CODE:\n{cleaned_tests}", "magenta"))
            final_test_code = cleaned_tests

        return {
            "generated_tests": final_test_code,
            "total_tokens": current_tokens + tokens
        }

    def _execution_node(self, state: AgentState):
        """
        Saves the file, runs pytest and processes the output.
        """
        self.logger.info(color_text("--- STEP 3: EXECUTING PYTEST ---", "cyan"))

        ok, err = syntax_check(state["generated_tests"])

        if not ok:
            self.logger.error(color_text(f"--- EXECUTION RESULT: Syntax Error ---", "red"))
            if self.verbose: self.logger.debug(err)
            return {
                "error": err,
                "syntax_error": True,
                "pytest_error": False,
                "failed_tests_infos": "",
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0,
                "iterations": state["iterations"] + 1,
            }

        report = run_pytest(state["target_module"], state["generated_tests"])

        if report["crash"] == "yes":
            self.logger.error(color_text(f"--- EXECUTION RESULT: Pytest Crash ---", "red"))
            if self.verbose: self.logger.debug(report["error_summary"])
            return {
                "error": report["error_summary"],
                "syntax_error": False,
                "pytest_error": True,
                "failed_tests_infos": "",
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0,
                "iterations": state["iterations"] + 1,
            }

        self.logger.info(color_text(
                f"--- EXECUTION RESULT: Coverage={report['coverage']}% {report['passed']} Passed {report['failed']} Failed ---",
                "green"
            )
        )
        if self.verbose:
            self.logger.debug(f"{report.get('failed_tests_infos','')}")

        return {
            "error": "",
            "syntax_error": False,
            "pytest_error": False,
            "failed_tests_infos": report["failed_tests_infos"],
            "coverage_percent": report["coverage"],
            "n_passed_tests": report["passed"],
            "n_failed_tests": report["failed"],
            "iterations": state["iterations"] + 1,
        }

    def _route_to(self, state: AgentState):
        if state["iterations"] >= state["max_iterations"]:
            return "end"

        if (state["pytest_error"] or state["syntax_error"] or state["n_failed_tests"] > 0):
            return "fix-tests"  

        current_cov = state.get("coverage_percent", 0)
        if current_cov < 100:
            return "replan" 

        return "end"

    def invoke(self):
        config = {"recursion_limit": 50}
        final_state = self.graph.invoke(self.initial_state, config=config) 

        output_filename = f"test_{Path(final_state['input_file_path']).stem}.py"
        output_file_path = (
            Path("data")
            / "output_tests"
            / self.output_dir
        )

        output_file_path.mkdir(parents=True, exist_ok=True)

        with open(str(output_file_path / output_filename), "w", encoding="utf-8") as f:
            f.write(final_state["generated_tests"])

        return final_state