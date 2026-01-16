from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import logging

from src.utils.code_parser import clean_llm_python, syntax_check
from src.utils.pytest_runner import run_pytest
from src.utils.file_manager import obtain_import_module_str, read_text


class SingleAgentChain:
    def __init__(self, input_file_path, output_dir, llm):
        """
        Inizializza l'agente singolo.
        """
        self.input_file_path = input_file_path
        self.output_dir = output_dir
        self.llm = llm
        self.target_module = obtain_import_module_str(input_file_path)
        self.code_under_test = read_text(input_file_path)
        self.logger = logging.getLogger("Agent")


    def _feed_the_chain(self):
        template = ChatPromptTemplate.from_messages([
        (
            "system", 
"""You are an expert Software Engineer in Test (SDET).
Your goal is to write a high-quality unit test suite using 'pytest' for the provided Python code.

While generating the output, you have to follow those instructions:
- **IMPORTANT**: Import the class or functions to test specifically from the module `{target_module}`. 
    (Example: `from {target_module} import ...`)
- Write the **minimum number of test cases** necessary to maximize code coverage. Prioritize coverage over test quantity.
- Ensure all test cases are **correct and fully functional**. Every test must pass.
- Cover success scenarios, edge cases, and error handling where relevant to achieving maximum coverage.
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
        
        # Extract tokens
        tokens = 0
        if hasattr(response, 'response_metadata'):
             tokens = response.response_metadata.get('token_usage', {}).get('total_tokens', 0)

        self.generated_tests = clean_llm_python(response.content)

        ok, err = syntax_check(self.generated_tests)

        if not ok:
            self.logger.error("--- EXECUTION RESULT: Syntax Error ---")
            return {
                "error": err,
                "failed_tests_infos": '',
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0,
                "total_tokens": tokens
            }

        report = run_pytest(self.target_module, self.generated_tests)

        if report["crash"] == 'yes':
            self.logger.error("--- EXECUTION RESULT: Pytest Crash ---")

            return {
                "error": report["error_summary"],
                "failed_tests_infos": '',
                "coverage_percent": 0,
                "n_passed_tests": 0,
                "n_failed_tests": 0,
                "total_tokens": tokens
            }
        
        self.logger.info(f"--- EXECUTION RESULT: Coverage={report['coverage']}% {report['passed']} Passed {report['failed']} Failed ---")
        
        return {
            "error": '',
            "failed_tests_infos": report["failed_tests_infos"],
            "coverage_percent": report["coverage"],
            "n_passed_tests": report["passed"],
            "n_failed_tests": report["failed"],
            "total_tokens": tokens
        }


    def invoke(self):
        chain_result = self._feed_the_chain()

        output_filename = f"test_{Path(self.input_file_path).stem}.py"
        output_file_path = (
            Path("data")
            / "output_tests"
            / self.output_dir
        )

        output_file_path.mkdir(parents=True, exist_ok=True)

        with open(str(output_file_path / output_filename), "w") as f:
            f.write(self.generated_tests)

        return chain_result