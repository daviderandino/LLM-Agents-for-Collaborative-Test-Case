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
        "failed_tests_infos": '',     # List of "FAILED name - error" strings
        "error_summary": ''           # Used only if status == crash
    }

    # It's hard for pytest to actually crash
    if exit_code > 1:
        report["crash"] = "yes"
        report["error_summary"] = stderr
        return report

    # coverage in stdout -> pytest was executed successfully
    cov_match = re.search(r"^TOTAL\s+.*?\s+(\d+)%\s*$", stdout, re.MULTILINE)

    if cov_match:
        # If found the line, extract the number
        report["coverage"] = int(cov_match.group(1))
    else:
        # If NOT found (e.g. badly failed tests), set to 0 and don't crash
        report["coverage"] = 0

    # Extract the failed tests
    fail_pattern = r"(FAILED|ERROR)\s+.*?::(\S+)\s+(?:-\s+)?(.*)"
    
    failed_tests = []
    
    for line in stdout.splitlines():
        clean_line = line.strip()
        
        # FIX 1: Check both FAILED and ERROR
        if clean_line.startswith(("FAILED", "ERROR")):
            match = re.search(fail_pattern, clean_line)
            if match:
                # FIX 2: Updated indices
                status = match.group(1)    # "FAILED" or "ERROR"
                test_name = match.group(2) # The test name
                error_msg = match.group(3) # The rest of the line
                
                # Dynamic formatting: "FAILED name - msg" or "ERROR name - msg"
                failed_tests.append(f"{status} {test_name} - {error_msg}")

    # Concatenate into a single string containing failed tests
    report["failed_tests_infos"] = "\n".join(failed_tests)

    # Count passed/failed tests
    passed_m = re.search(r"(\d+) passed", stdout)
    failed_m = re.search(r"(\d+) failed", stdout)
    error_m = re.search(r"(\d+) error", stdout)

    report["passed"] = int(passed_m.group(1)) if passed_m else 0
    val_failed = int(failed_m.group(1)) if failed_m else 0
    val_error = int(error_m.group(1)) if error_m else 0
    report["failed"] = val_failed + val_error

    return report
