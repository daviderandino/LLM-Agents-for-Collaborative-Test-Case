from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import os

from src.utils.code_parser import clean_llm_python, syntax_check
from src.utils.pytest_runner import run_pytest
from src.utils.file_manager import obtain_import_module_str, read_text


class SingleAgentChain:
    def __init__(self, input_file_path, llm):
        """
        Inizializza l'agente singolo.
        """
        self.input_file_path = input_file_path
        self.llm = llm
        self.target_module = obtain_import_module_str(input_file_path)
        self.code_under_test = read_text(input_file_path)


    def _feed_the_chain(self):
        template = ChatPromptTemplate.from_messages([
        (
            "system", 
"""You are an expert Software Engineer in Test (SDET).
Your goal is to write a high-quality unit test suite using 'pytest' for the provided Python code.

While generating the output, you have to follow those three instructions:
- **IMPORTANT**: Import the class or functions to test specifically from the module `{target_module}`. 
    (Example: `from {target_module} import ...`)
- Write test cases for success scenarios, edge cases, and error handling.
- Output ONLY the raw Python code. Do not include markdown formatting or explanations."""
        ),
        (
            "human", 
"""Write a unit test suite for the Python code below:

{code_under_test}"""
        ),
        ])

        chain = template | self.llm
        chain_input = {
            "code_under_test": self.code_under_test,
            "target_module": self.target_module
        }

        response = chain.invoke(chain_input)

        self.cleaned_tests = clean_llm_python(response.content)

        ok, err = syntax_check(self.cleaned_tests)

        if not ok:
            print(f"--- EXECUTION RESULT: Syntax Error ---")
            return {
                "error": err,
                "failed_tests_infos": '',
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0
            }

        report = run_pytest(self.target_module, self.cleaned_tests)

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


    def invoke(self):
        chain_result = self._feed_the_chain()

        output_filename = f"test_{Path(self.input_file_path).stem}.py"
        output_file_path = os.path.join("data", "output_tests", "single_agent", output_filename)
        
        with open(output_file_path, "w") as f:
            f.write(self.cleaned_tests)

        return chain_result