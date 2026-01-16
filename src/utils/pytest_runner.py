from __future__ import annotations

import re
import sys
import subprocess
import os


def parse_coverage_percent(output: str) -> int:

    m = re.search(r"^TOTAL.*?(\d+)%\s*$", output, re.MULTILINE)
    if m:
        return int(m.group(1))
    m2 = re.search(r"(\d+)%\s*$", output, re.MULTILINE)
    return int(m2.group(1)) if m2 else 0


def run_pytest(target_module, generated_tests):

    with open("tmp_test.py", "w",encoding="utf-8") as f:
        f.write(generated_tests)

    cmd = [
        sys.executable, "-m", "pytest",
        "tmp_test.py",
        f"--cov={target_module}",
        "--tb=line",
        "--color=no",
        "-vv"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        stdout = result.stdout
        stderr = result.stderr
        exit_code = result.returncode
        
        report = analyze_pytest_output(stdout, stderr, exit_code)

        return report

    finally:
        os.remove("tmp_test.py")


def analyze_pytest_output(stdout, stderr, exit_code):
    report = {
        "crash": "no",                # yes | no
        "coverage": 0,
        "passed": 0,
        "failed": 0,
        "failed_tests_infos": '',     # Lista di stringhe "FAILED nome - errore"
        "error_summary": ''           # Usato solo se status == crash
    }

    # è difficile che pytest proprio crashi
    if exit_code > 1:
        report["crash"] = "yes"
        report["error_summary"] = stderr
        return report

    # coverage in stdout -> pytest è stato eseguito con successo
    cov_match = re.search(r"^TOTAL\s+.*?\s+(\d+)%\s*$", stdout, re.MULTILINE)

    if cov_match:
        # Se ha trovato la riga, estrai il numero
        report["coverage"] = int(cov_match.group(1))
    else:
        # Se NON l'ha trovata (es. test falliti male), metti 0 e non crashare
        report["coverage"] = 0

    # estraiamo i test falliti
    fail_pattern = r"(FAILED|ERROR)\s+.*?::(\S+)\s+(?:-\s+)?(.*)"
    
    failed_tests = []
    
    for line in stdout.splitlines():
        clean_line = line.strip()
        
        # CORREZIONE 1: Controlliamo sia FAILED che ERROR
        if clean_line.startswith(("FAILED", "ERROR")):
            match = re.search(fail_pattern, clean_line)
            if match:
                # CORREZIONE 2: Indici aggiornati
                status = match.group(1)    # "FAILED" o "ERROR"
                test_name = match.group(2) # Il nome del test
                error_msg = match.group(3) # Il resto della riga
                
                # Formattazione dinamica: "FAILED nome - msg" oppure "ERROR nome - msg"
                failed_tests.append(f"{status} {test_name} - {error_msg}")

    # concateno in un'unica stringa che contiene i test non passati
    report["failed_tests_infos"] = "\n".join(failed_tests)

    # conteggio test passati/falliti
    passed_m = re.search(r"(\d+) passed", stdout)
    failed_m = re.search(r"(\d+) failed", stdout)
    error_m = re.search(r"(\d+) error", stdout)

    report["passed"] = int(passed_m.group(1)) if passed_m else 0
    report["failed"] = int(failed_m.group(1)) if failed_m else 0 + int(error_m.group(1)) if error_m else 0

    return report
