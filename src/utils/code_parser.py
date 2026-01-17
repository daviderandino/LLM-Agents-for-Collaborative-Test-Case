import re
import ast


def clean_llm_python(text: str) -> str:
    """
    Extracts Python code from Markdown blocks using Regex.
    Removes all text before and after the code block.
    """
    # Pattern that searches for ```python (optional) ...content... ```
    # re.DOTALL allows the dot (.) to include newlines as well
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    code = m.group(1) if m else text
    # Remove residue
    code = code.replace("```python", "").replace("```", "").strip()
    return code


def ensure_pytest_import(code: str) -> str:
    # Ensures that the pytest import is present in the code
    if re.search(r"^\s*import\s+pytest\b", code, re.MULTILINE):
        return code
    return "import pytest\n\n" + code.lstrip()


def syntax_check(code: str) -> tuple[bool, str]:
    # Checks if the Python code has syntax errors
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg}"


def remove_failed_tests(code: str, failed_tests_infos: str) -> str:
    """
    Parses the failed test report to extract function names, then uses AST 
    to remove those function definitions from the code string.
    """
    failed_names = set()
    # Regex matches "FAILED test_name -" or "ERROR test_name -"
    for line in failed_tests_infos.splitlines():
        m = re.search(r"(?:FAILED|ERROR)\s+(\S+)", line)
        if m:
            # Estrae il nome grezzo (es. "tests/test_file.py::test_div[10-0]")
            raw_name = m.group(1).split("::")[-1]
            
            # RIMUOVE i parametri parametrizzati (es. "test_div[10-0]" -> "test_div")
            test_name = raw_name.split("[")[0]
            
            failed_names.add(test_name)

    if not failed_names:
        return code

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code

    lines = code.splitlines(keepends=True)
    ranges_to_remove = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in failed_names:
            # ast lineno is 1-based, we want 0-based for list slicing
            start_line = node.lineno - 1
            end_line = node.end_lineno  # inclusive in ast
            
            # If the function has decorators, we want to remove them too.
            # Usually node.lineno points to the first decorator if present in newer python versions,
            # but to be safe we can check the decorator_list
            if node.decorator_list:
                start_line = min(d.lineno for d in node.decorator_list) - 1
            
            ranges_to_remove.append((start_line, end_line))

    # Sort descending to remove from bottom up to avoid shifting indices
    ranges_to_remove.sort(key=lambda x: x[0], reverse=True)

    for start, end in ranges_to_remove:
        # Check for preceding empty lines to clean up spacing
        # (Optional refinement)
        del lines[start:end]

    return "".join(lines)