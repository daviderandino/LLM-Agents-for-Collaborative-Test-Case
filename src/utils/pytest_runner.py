from __future__ import annotations

import re
import sys
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class PytestRunResult:
    output: str
    returncode: int
    coverage_percent: int
    error_occurred: bool


def parse_coverage_percent(output: str) -> int:
    
    # Estrae la coverage percent dall'output di pytest-cov.
    # Regex cerca un numero percentuale alla fine della riga che inizia con TOTAL, poi fallback
    # Nota: l'output varia leggermente in base alla versione, questa regex è generica

    m = re.search(r"^TOTAL.*?(\d+)%\s*$", output, re.MULTILINE)
    if m:
        return int(m.group(1))

    # Fallback di sicurezza:
    # in alcuni casi pytest-cov non stampa la riga "TOTAL" (es. crash dei test,
    # versioni diverse del plugin, report parziale).
    # In questi casi recuperiamo l’ultima percentuale presente nell’output
    # per evitare falsi negativi (coverage=0) e loop inutili dell’agent.
    m2 = re.search(r"(\d+)%\s*$", output, re.MULTILINE)
    return int(m2.group(1)) if m2 else 0


def run_pytest_with_coverage(
    *,
    project_root: str,
    test_filename: str,
    cov_target: str,
    timeout: int = 30,
    extra_args: Optional[list[str]] = None,
) -> PytestRunResult:
    
    # Esegue pytest con coverage usando lo stesso interprete Python dell'agent.
    #  - project_root: cwd del subprocess
    #  - test_filename: nome o path relativo al cwd (es: "temp_test_execution.py")
    #  - cov_target: modulo (es: "data.input_code.bank_account")
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_filename,
        f"--cov={cov_target}",
        "--cov-report=term-missing",
        "--cov-report=html",
    ]
    if extra_args:
        cmd.extend(extra_args)

    try:
        r = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = (r.stdout or "") + (r.stderr or "")
        is_error = r.returncode != 0
        cov = parse_coverage_percent(output)

        # --- DEBUG PRINT ---
        if is_error:
            print("\n!!! PYTEST FAILURE OUTPUT !!!")
            # Stampiamo solo le ultime 10 righe dell'errore per non intasare la console
            print('\n'.join(output.splitlines()[-15:]))
            print("!!! END FAILURE OUTPUT !!!\n")

        return PytestRunResult(
            output=output,
            returncode=r.returncode,
            coverage_percent=cov,
            error_occurred=is_error,
        )
    except Exception as e:
        output = f"EXCEPTION DURING EXECUTION: {e}"
        return PytestRunResult(
            output=output,
            returncode=999,
            coverage_percent=0,
            error_occurred=True,
        )
