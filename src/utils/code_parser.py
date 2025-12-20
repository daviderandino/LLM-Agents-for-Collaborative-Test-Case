import re
import ast


def clean_llm_python(text: str) -> str:
    """
    Estrae il codice Python dai blocchi Markdown usando Regex.
    Rimuove tutto il testo prima e dopo il blocco di codice.
    """
    # Pattern che cerca ```python (opzionale) ...contenuto... ```
    # re.DOTALL permette al punto (.) di includere anche le nuove righe
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    code = m.group(1) if m else text
    # Rimuove residui
    code = code.replace("```python", "").replace("```", "").strip()
    return code


def ensure_pytest_import(code: str) -> str:
    # Assicura che l'import di pytest sia presente nel codice
    if re.search(r"^\s*import\s+pytest\b", code, re.MULTILINE):
        return code
    return "import pytest\n\n" + code.lstrip()


def syntax_check(code: str) -> tuple[bool, str]:
    # Controlla se il codice Python ha errori di sintassi
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg}"
