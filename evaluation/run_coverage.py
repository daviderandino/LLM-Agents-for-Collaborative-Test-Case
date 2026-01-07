"""
Script to compute test coverage.

Utility functions for running pytest-cov and analyzing coverage results.
"""

from __future__ import annotations

import re
import sys
import subprocess
import os
import json
from pathlib import Path
from typing import Optional


def run_coverage(
    source_module: str,
    test_file: str,
    cwd: Optional[str] = None,
    html_report: bool = False,
    xml_report: bool = False,
    json_report: bool = False
) -> dict:
    """
    Runs pytest with coverage on a specific test file against a source module.
    
    Args:
        source_module: Path to the source module to measure coverage for 
                       (e.g., 'data/input_code/library.py' or 'data.input_code.library')
        test_file: Path to the test file to run
        cwd: Working directory for running the command (defaults to project root)
        html_report: If True, generates an HTML coverage report
        xml_report: If True, generates an XML coverage report (useful for CI)
        json_report: If True, generates a JSON coverage report
        
    Returns:
        Dictionary with coverage results:
        {
            "success": bool,
            "coverage_percent": int,
            "covered_lines": int,
            "total_lines": int,
            "missing_lines": str,
            "passed_tests": int,
            "failed_tests": int,
            "error_tests": int,
            "stdout": str,
            "stderr": str
        }
    """
    # Build the pytest command with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        test_file,
        f"--cov={source_module}",
        "--cov-report=term-missing",
        "--tb=short",
        "--color=no",
        "-v"
    ]
    
    # Add optional report formats
    if html_report:
        cmd.append("--cov-report=html")
    if xml_report:
        cmd.append("--cov-report=xml")
    if json_report:
        cmd.append("--cov-report=json")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        
        return _parse_coverage_output(result.stdout, result.stderr, result.returncode)
        
    except Exception as e:
        return {
            "success": False,
            "coverage_percent": 0,
            "covered_lines": 0,
            "total_lines": 0,
            "missing_lines": "",
            "passed_tests": 0,
            "failed_tests": 0,
            "error_tests": 0,
            "stdout": "",
            "stderr": str(e)
        }


def _parse_coverage_output(stdout: str, stderr: str, exit_code: int) -> dict:
    """
    Parses the output from pytest-cov to extract coverage metrics.
    
    Args:
        stdout: Standard output from pytest
        stderr: Standard error from pytest
        exit_code: Exit code from pytest
        
    Returns:
        Dictionary with parsed coverage results
    """
    report = {
        "success": exit_code <= 1,  # 0 = all passed, 1 = some failed, >1 = error
        "coverage_percent": 0,
        "covered_lines": 0,
        "total_lines": 0,
        "missing_lines": "",
        "passed_tests": 0,
        "failed_tests": 0,
        "error_tests": 0,
        "stdout": stdout,
        "stderr": stderr
    }
    
    # Extract coverage percentage from TOTAL line
    # Format: TOTAL    123    45    63%    1-5, 10-15
    total_match = re.search(
        r"^TOTAL\s+(\d+)\s+(\d+)\s+(\d+)%(?:\s+(.*))?$",
        stdout,
        re.MULTILINE
    )
    
    if total_match:
        report["total_lines"] = int(total_match.group(1))
        missed = int(total_match.group(2))
        report["covered_lines"] = report["total_lines"] - missed
        report["coverage_percent"] = int(total_match.group(3))
        report["missing_lines"] = total_match.group(4) or ""
    else:
        # Fallback: try to find any percentage
        pct_match = re.search(r"(\d+)%\s*$", stdout, re.MULTILINE)
        if pct_match:
            report["coverage_percent"] = int(pct_match.group(1))
    
    # Extract test counts
    passed_match = re.search(r"(\d+)\s+passed", stdout)
    failed_match = re.search(r"(\d+)\s+failed", stdout)
    error_match = re.search(r"(\d+)\s+error", stdout)
    
    report["passed_tests"] = int(passed_match.group(1)) if passed_match else 0
    report["failed_tests"] = int(failed_match.group(1)) if failed_match else 0
    report["error_tests"] = int(error_match.group(1)) if error_match else 0
    
    return report


def run_coverage_batch(
    test_configs: list[dict],
    cwd: Optional[str] = None
) -> list[dict]:
    """
    Runs coverage analysis for multiple source/test file pairs.
    
    Args:
        test_configs: List of dicts with 'source_module' and 'test_file' keys
        cwd: Working directory for running commands
        
    Returns:
        List of coverage results for each configuration
    """
    results = []
    for config in test_configs:
        result = run_coverage(
            source_module=config["source_module"],
            test_file=config["test_file"],
            cwd=cwd
        )
        result["config"] = config
        results.append(result)
    return results


def get_coverage_summary(results: list[dict]) -> dict:
    """
    Generates a summary of coverage results.
    
    Args:
        results: List of coverage result dictionaries
        
    Returns:
        Summary dictionary with aggregate statistics
    """
    if not results:
        return {"error": "No results to summarize"}
    
    coverages = [r["coverage_percent"] for r in results if r["success"]]
    
    return {
        "total_files": len(results),
        "successful_runs": len(coverages),
        "failed_runs": len(results) - len(coverages),
        "average_coverage": sum(coverages) / len(coverages) if coverages else 0,
        "min_coverage": min(coverages) if coverages else 0,
        "max_coverage": max(coverages) if coverages else 0,
        "total_passed_tests": sum(r["passed_tests"] for r in results),
        "total_failed_tests": sum(r["failed_tests"] for r in results),
    }


def print_coverage_report(result: dict, verbose: bool = True) -> None:
    """
    Prints a formatted coverage report to stdout.
    
    Args:
        result: Coverage result dictionary
        verbose: If True, prints detailed output
    """
    print("\n" + "=" * 60)
    print("COVERAGE REPORT")
    print("=" * 60)
    
    if result.get("config"):
        print(f"Source: {result['config']['source_module']}")
        print(f"Tests:  {result['config']['test_file']}")
    
    print(f"\nCoverage: {result['coverage_percent']}%")
    print(f"Lines:    {result['covered_lines']}/{result['total_lines']}")
    
    if result["missing_lines"]:
        print(f"Missing:  {result['missing_lines']}")
    
    print(f"\nTests: {result['passed_tests']} passed, "
          f"{result['failed_tests']} failed, "
          f"{result['error_tests']} errors")
    
    if verbose and result.get("stdout"):
        print("\n" + "-" * 60)
        print("DETAILED OUTPUT:")
        print("-" * 60)
        print(result["stdout"])
    
    print("=" * 60 + "\n")


# Main execution for standalone usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run coverage analysis on test files")
    parser.add_argument("--source", "-s", required=True, help="Source module to measure")
    parser.add_argument("--test", "-t", required=True, help="Test file to run")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--xml", action="store_true", help="Generate XML report")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    result = run_coverage(
        source_module=args.source,
        test_file=args.test,
        html_report=args.html,
        xml_report=args.xml,
        json_report=args.json
    )
    
    print_coverage_report(result, verbose=not args.quiet)
