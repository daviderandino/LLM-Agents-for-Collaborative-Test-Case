from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import logging
import time

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
                    "Role: Senior Python QA Engineer and Test Planner.\n"
                    "Task: Analyze the provided code and create a comprehensive list of test scenarios in natural language.\n\n"
                    "Your Mission:\n"
                    "1. Read and understand the target function/class thoroughly.\n"
                    "2. Identify all logical paths (branches, conditions, loops).\n"
                    "3. Identify edge cases (boundary values, empty inputs, None, special conditions).\n"
                    "4. Create a clear, numbered list of test scenarios to cover all paths and edge cases.\n\n"
                    "Strategy for Maximum Coverage:\n"
                    "- Branch Analysis: Every `if`, `elif`, `else`, loop entry/exit needs a scenario.\n"
                    "- Boundary Values: MIN, MAX, MIN-1, MAX+1, ZERO, NONE, empty collections.\n"
                    "- Exception Paths: Every possible exception that can be raised.\n"
                    "- Happy Path: Normal expected usage.\n\n"
                    "Output Format:\n"
                    "A numbered list of test scenarios in natural language. Each scenario should describe:\n"
                    "- What to test (function/method name)\n"
                    "- What inputs to use\n"
                    "- What behavior/output to expect\n"
                    "- Why this scenario is important (coverage rationale)\n\n"
                    "Example:\n"
                    "1. Test div with normal positive numbers (a=10, b=2) - should return 5.0 [Happy path]\n"
                    "2. Test div with zero divisor (a=5, b=0) - should raise ValueError [Exception handling]\n"
                    "3. Test div with negative numbers (a=-10, b=2) - should return -5.0 [Negative input path]\n\n"
                    "Strict Rules:\n"
                    "1. Use natural language, be clear and specific.\n"
                    "2. Number each scenario.\n"
                    "3. Be comprehensive but avoid redundancy.",
                ),
                # FEW-SHOT (Input Code -> Output Scenarios)
                (
                    "human",
                    "Analyze:\ndef div(a, b):\n    if b == 0: raise ValueError()\n    return a / b",
                ),
                (
                    "ai",
                    "1. Test div with normal positive numbers (a=10, b=2) - should return 5.0 [Happy path, normal execution]\n"
                    "2. Test div with zero divisor (a=5, b=0) - should raise ValueError [Exception path, boundary condition]\n"
                    "3. Test div with negative dividend (a=-10, b=2) - should return -5.0 [Negative input handling]\n"
                    "4. Test div with negative divisor (a=10, b=-2) - should return -5.0 [Negative divisor path]\n"
                    "5. Test div with both negative (a=-10, b=-2) - should return 5.0 [Both negative edge case]",
                ),
                # REAL INPUT: Just the source code
                (
                    "human",
                    "Analyze the following Python code:\n"
                    "```python\n"
                    "{code}\n"
                    "```"
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
                    "Role: Python Coverage Specialist and Gap Analyzer.\n"
                    "Context: The previous test suite failed to achieve 100% coverage.\n"
                    "Objective: Analyze the Source Code AND the Existing Tests to find MISSED logical paths.\n"
                    "Task: Create ONLY new test scenarios needed to fill the coverage gaps.\n"
                    "Key Constraint: Minimize test count while maximizing coverage - add only essential scenarios.\n\n"
                    "Strategy for Gap Filling:\n"
                    "1. Deep Analysis: Compare Source Code vs Existing Tests to spot uncovered branches.\n"
                    "2. Complex Logic: Focus on compound conditions (AND/OR) and edge boundaries missed by current tests.\n"
                    "3. No Duplicates: Do NOT regenerate scenarios that are already tested.\n\n"
                    "Output Format:\n"
                    "A numbered list of NEW test scenarios in natural language. Each scenario should describe:\n"
                    "- What to test (function/method name)\n"
                    "- What inputs to use\n"
                    "- What behavior/output to expect\n"
                    "- Why this fills a coverage gap\n\n"
                    "Strict Rules:\n"
                    "1. Use natural language, be clear and specific.\n"
                    "2. Number each scenario (continue numbering from existing scenarios).\n"
                    "3. Only include scenarios that test paths NOT covered by existing tests.",
                ),
                # FEW-SHOT 
                (
                    "human",
                    "Analyze code:\ndef check(x):\n    if x > 0 and x < 10:\n        return True\n    return False\n\nExisting tests cover: x=5 (returns True)",
                ),
                (
                    "ai",
                    "6. Test check with boundary value at upper limit (x=10) - should return False [Missed upper boundary]\n"
                    "7. Test check with negative value (x=-1) - should return False [Missed negative input path]\n"
                    "8. Test check with zero (x=0) - should return False [Missed zero boundary]",
                ),
                # INPUT REALE
                (
                    "human",
                    "Previous coverage was insufficient ({current_cov}%).\n\n"
                    "SOURCE CODE:\n"
                    "```python\n"
                    "{code}\n"
                    "```"
                    "EXISTING TESTS (Do not regenerate these):\n{current_tests}\n\n"
                    "Identify the missing gaps and create NEW test scenarios only.",
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

            # --- APPEND LOGIC FOR NATURAL LANGUAGE SCENARIOS ---
            new_plan_fragment = response.content.strip()
            old_plan = state.get("test_plan", "").strip()
            
            # Simple concatenation with newline separator
            if old_plan:
                updated_full_plan = old_plan + "\n" + new_plan_fragment
            else:
                updated_full_plan = new_plan_fragment

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
        self.logger.info(color_text("--- WAITING 10 SECONDS BEFORE DEVELOPER ---", "yellow"))
        time.sleep(10)
        
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
                    "Role: Senior Pytest Engineer.\n"
                    "Task: Implement test cases based on natural language test scenarios.\n"
                    "Key Objectives:\n"
                    "- Implement ALL scenarios described in the test plan.\n"
                    "- Ensure all test cases are correct and fully functional. Every test must pass.\n"
                    "- Generate efficient, production-grade test code.\n\n"
                    "Strict Rules:\n"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source code. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the code to test.\n"
                    "- 2. Strategy: Group similar tests with `@pytest.mark.parametrize` where possible.\n"
                    "- 3. Exceptions: Use `with pytest.raises(ExceptionType):` for exception scenarios.\n"
                    "- 4. Assertions: Use appropriate assertions (`assert`, `assert ==`, `assert in`, etc.).\n"
                    "- 5. Classes: If testing a method, instantiate the class first.\n"
                    "- 6. Output: Start output with exactly: ```python, and end output with exactly: ```. No explanatory text.",
                ),
                (
                    "human",
                    "Scenarios:\n1. Test div with normal positive numbers (a=10, b=2) - should return 5.0\n2. Test div with zero divisor (a=5, b=0) - should raise ZeroDivisionError\n\nCode: def div(a,b): return a/b",
                ),
                (
                    "ai",
                    "```python\nimport pytest\nfrom calc import *\n\n@pytest.mark.parametrize('a, b, expected', [\n    (10, 2, 5.0)\n])\ndef test_div_success(a, b, expected):\n    assert div(a, b) == expected\n\ndef test_div_zero_error():\n    with pytest.raises(ZeroDivisionError):\n        div(5, 0)\n```",
                ),
                (
                    "human", 
                    "Test Scenarios:\n{plan}\n\nCode to test:\n"
                    "```python\n"
                    "{code}\n"
                    "```"
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
                    "Role: Senior Pytest Debugger.\n"
                    "Task: Fix only the failing tests to achieve 100% pass rate.\n"
                    "Strategy:\n"
                    "- 1. Analyze the Pytest failure report.\n"
                    "- 2. Compare expectations vs actual Source Code behavior.\n"
                    "- 3. ADJUST the test assertions/setup to match the Source Code reality.\n"
                    "Key Objectives:\n"
                    "- Ensure all test cases are correct and fully functional. Every test must pass.\n"
                    "Strict Rules:\n"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the source code.\n"
                    "- 2. Strategy: Group tests with `@pytest.mark.parametrize` where possible.\n"
                    "- 3. Exceptions: Use `with pytest.raises(ExceptionType):` for exception cases.\n"
                    "- 4. Classes: If target is `Class.method`, instantiate the class first.\n"
                    "- 5. Output: Start output with exactly: ```python, and end output with exactly: ```. No text.",
                ),
                (
                    "human",
                    "Source Code (Truth):\n"
                    "```python\n"
                    "{code}\n"
                    "```"
                    "Current Test Code:\n"
                    "```python\n"
                    "{previous_test_code}\n"
                    "```"
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
                    "Role: Python Code Fixer.\n"
                    "Task: Fix the syntax/runtime error in the provided test file.\n"
                    "Key Objectives:\n"
                    "- Ensure all test cases are correct and fully functional. Every test must pass.\n"
                    "Strict Rules:\n"
                    "- 1. Imports: Always start with `import pytest` and `from {target_module} import *`. Import any other lib used in source. DO NOT invent new classes or functions. Use ONLY the exact classes or functions names found in the source code.\n"
                    "- 2. Strategy: Group tests with `@pytest.mark.parametrize` where possible.\n"
                    "- 3. Exceptions: Use `with pytest.raises(ExceptionType):` for exception cases.\n"
                    "- 4. Classes: If target is `Class.method`, instantiate the class first.\n"
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
                    "Role: Senior Pytest Engineer (Extension Mode).\n"
                    "Task: Write ONLY the NEW test functions for the scenarios provided, to append to the existing suite.\n"
                    "Key Objectives:\n"
                    "- Implement ONLY the new test scenarios described.\n"
                    "- Ensure all test cases are correct and fully functional. Every test must pass.\n"
                    "- Do NOT duplicate existing tests.\n\n"
                    "Strict Rules:\n"
                    "- 1. DO NOT include imports - they already exist in the file.\n"
                    "- 2. Write ONLY new test functions based on the new scenarios.\n"
                    "- 3. Strategy: Group similar tests with `@pytest.mark.parametrize` where possible.\n"
                    "- 4. Exceptions: Use `with pytest.raises(ExceptionType):` for exception scenarios.\n"
                    "- 5. Assertions: Use appropriate assertions matching the scenario description.\n"
                    "- 6. Output: Start output with exactly: ```python, and end output with exactly: ```. No text.",
                ),
                (
                    "human",
                    "Source Code (Truth):\n"
                    "```python\n"
                    "{code}\n"
                    "```"
                    "Current Test Code:\n"
                    "```python\n"
                    "{previous_test_code}\n"
                    "```"
                    "New Test Scenarios (to implement):\n{plan}\n\nGenerate ONLY the python code for the NEW test functions to be appended.",
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