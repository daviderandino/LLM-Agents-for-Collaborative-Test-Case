"""
Script used for mutation testing.

Utility functions for running mutmut mutation testing and analyzing results.
"""

from __future__ import annotations

import re
import sys
import subprocess
import os
import json
from pathlib import Path
from typing import Optional


def run_mutation_testing(
    source_file: str,
    test_file: str,
    cwd: Optional[str] = None,
    timeout: int = 300,
    runner: str = "pytest"
) -> dict:
    """
    Runs mutmut mutation testing on a source file using a test file.
    
    Args:
        source_file: Path to the source file to mutate (e.g., 'data/input_code/library.py')
        test_file: Path to the test file to run against mutations
        cwd: Working directory for running the command (defaults to project root)
        timeout: Timeout in seconds for the entire mutation run
        runner: Test runner to use ('pytest' is default)
        
    Returns:
        Dictionary with mutation testing results:
        {
            "success": bool,
            "killed": int,
            "survived": int,
            "timeout": int,
            "suspicious": int,
            "skipped": int,
            "total_mutants": int,
            "mutation_score": float,  # killed / (killed + survived) * 100
            "stdout": str,
            "stderr": str
        }
    """
    # Clean any previous mutmut cache to start fresh
    _clean_mutmut_cache(cwd)
    
    # Build the mutmut run command (mutmut 2.x syntax)
    cmd = [
        sys.executable, "-m", "mutmut", "run",
        "--paths-to-mutate", source_file,
        "--tests-dir", str(Path(test_file).parent),
        "--runner", f"{runner} {test_file}",
        "--no-progress",
        "--simple-output"
    ]
    
    # Set PYTHONPATH to include the working directory for imports
    env = os.environ.copy()
    if cwd:
        current_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{cwd}:{current_pythonpath}" if current_pythonpath else cwd
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout,
            env=env
        )
        
        # Parse results from mutmut output
        parsed = _parse_mutmut_output(result.stdout, result.stderr, result.returncode)
        
        # If mutmut failed (tests don't run cleanly), don't read from cache
        if parsed.get("_skip_cache"):
            del parsed["_skip_cache"]
            return parsed
        
        # If parsing from output didn't work, try reading from cache database
        cache_stats = _get_mutmut_stats_from_cache(cwd)
        if cache_stats and cache_stats.get("total_mutants", 0) > 0:
            parsed["killed"] = cache_stats.get("killed", 0)
            parsed["survived"] = cache_stats.get("survived", 0)
            parsed["timeout"] = cache_stats.get("timeout", 0)
            parsed["suspicious"] = cache_stats.get("suspicious", 0)
            parsed["skipped"] = cache_stats.get("skipped", 0)
            parsed["total_mutants"] = cache_stats.get("total_mutants", 0)
            parsed["mutation_score"] = cache_stats.get("mutation_score", 0.0)
        else:
            # Fallback: Get detailed results from mutmut results command
            results_detail = _get_mutmut_results(cwd, env)
            if results_detail:
                parsed.update(results_detail)
            
            # Recalculate mutation score after updating counts
            denominator = parsed["killed"] + parsed["survived"]
            if denominator > 0:
                parsed["mutation_score"] = round((parsed["killed"] / denominator) * 100, 2)
        
        return parsed
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "killed": 0,
            "survived": 0,
            "timeout": 0,
            "suspicious": 0,
            "skipped": 0,
            "total_mutants": 0,
            "mutation_score": 0.0,
            "stdout": "",
            "stderr": f"Mutation testing timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "killed": 0,
            "survived": 0,
            "timeout": 0,
            "suspicious": 0,
            "skipped": 0,
            "total_mutants": 0,
            "mutation_score": 0.0,
            "stdout": "",
            "stderr": str(e)
        }


def _clean_mutmut_cache(cwd: Optional[str] = None) -> None:
    """
    Cleans the mutmut cache file.
    
    Args:
        cwd: Working directory where cache might exist
    """
    cache_path = Path(cwd or ".") / ".mutmut-cache"
    if cache_path.exists():
        if cache_path.is_file():
            cache_path.unlink()  # Remove file
        else:
            import shutil
            shutil.rmtree(cache_path, ignore_errors=True)  # Remove directory


def _parse_mutmut_output(stdout: str, stderr: str, exit_code: int) -> dict:
    """
    Parses the output from mutmut run command.
    
    Args:
        stdout: Standard output from mutmut
        stderr: Standard error from mutmut
        exit_code: Exit code from mutmut
        
    Returns:
        Dictionary with parsed mutation results
    """
    report = {
        "success": exit_code != 1,  # exit 1 = fatal error, 0 or 2/4/8 = success
        "killed": 0,
        "survived": 0,
        "timeout": 0,
        "suspicious": 0,
        "skipped": 0,
        "total_mutants": 0,
        "mutation_score": 0.0,
        "stdout": stdout,
        "stderr": stderr
    }
    
    # Check for fatal error (tests don't pass without mutations)
    if "Tests don't run cleanly without mutations" in stdout or "Tests don't run cleanly without mutations" in stderr:
        report["success"] = False
        report["stderr"] = "Tests don't run cleanly without mutations. Some tests are failing."
        # Don't read from cache when mutmut fails - cache may have stale data
        report["_skip_cache"] = True
        return report
    
    # Try to parse the summary at the end
    # Format varies, common patterns:
    # "X mutants killed, Y survived, Z timed out"
    summary_patterns = [
        r"(\d+)\s*(?:mutants?\s+)?killed",
        r"(\d+)\s*(?:mutants?\s+)?survived",
        r"(\d+)\s*(?:mutants?\s+)?(?:timed?\s*out|timeout)",
        r"(\d+)\s*(?:mutants?\s+)?suspicious",
        r"(\d+)\s*(?:mutants?\s+)?skipped",
    ]
    
    killed_match = re.search(summary_patterns[0], stdout, re.IGNORECASE)
    survived_match = re.search(summary_patterns[1], stdout, re.IGNORECASE)
    timeout_match = re.search(summary_patterns[2], stdout, re.IGNORECASE)
    suspicious_match = re.search(summary_patterns[3], stdout, re.IGNORECASE)
    skipped_match = re.search(summary_patterns[4], stdout, re.IGNORECASE)
    
    if killed_match:
        report["killed"] = int(killed_match.group(1))
    if survived_match:
        report["survived"] = int(survived_match.group(1))
    if timeout_match:
        report["timeout"] = int(timeout_match.group(1))
    if suspicious_match:
        report["suspicious"] = int(suspicious_match.group(1))
    if skipped_match:
        report["skipped"] = int(skipped_match.group(1))
    
    # Calculate totals
    report["total_mutants"] = (
        report["killed"] + report["survived"] + 
        report["timeout"] + report["suspicious"] + report["skipped"]
    )
    
    # Calculate mutation score (killed / (killed + survived))
    denominator = report["killed"] + report["survived"]
    if denominator > 0:
        report["mutation_score"] = round((report["killed"] / denominator) * 100, 2)
    
    return report


def _get_mutmut_stats_from_cache(cwd: Optional[str] = None) -> Optional[dict]:
    """
    Gets mutation statistics directly from the mutmut SQLite cache.
    
    Args:
        cwd: Working directory where .mutmut-cache exists
        
    Returns:
        Dictionary with counts for each status or None if unavailable
    """
    import sqlite3
    
    cache_path = Path(cwd or ".") / ".mutmut-cache"
    if not cache_path.exists():
        return None
    
    try:
        conn = sqlite3.connect(str(cache_path))
        cursor = conn.cursor()
        
        # Query the Mutant table for status counts
        # Status values in mutmut 2.x: 'ok_killed', 'bad_survived', 'bad_timeout', 'ok_suspicious', 'skipped', 'untested'
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM Mutant 
            GROUP BY status
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        stats: dict = {
            "killed": 0,
            "survived": 0,
            "timeout": 0,
            "suspicious": 0,
            "skipped": 0,
            "total_mutants": 0,
            "mutation_score": 0.0
        }
        
        # Map mutmut status values to our standard names
        status_mapping = {
            "ok_killed": "killed",
            "bad_survived": "survived",
            "bad_timeout": "timeout",
            "ok_suspicious": "suspicious",
            "skipped": "skipped"
        }
        
        for status, count in results:
            mapped_status = status_mapping.get(status)
            if mapped_status:
                stats[mapped_status] = count
        
        stats["total_mutants"] = stats["killed"] + stats["survived"] + stats["timeout"] + stats["suspicious"] + stats["skipped"]
        
        # Calculate mutation score
        denominator = stats["killed"] + stats["survived"]
        if denominator > 0:
            stats["mutation_score"] = round((stats["killed"] / denominator) * 100, 2)
        
        return stats
        
    except Exception:
        return None


def _get_mutmut_results(cwd: Optional[str] = None, env: Optional[dict] = None) -> Optional[dict]:
    """
    Gets detailed results using mutmut results command.
    
    Args:
        cwd: Working directory
        env: Environment variables to use
        
    Returns:
        Dictionary with detailed results or None if unavailable
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "mutmut", "results"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
            env=env
        )
        
        if result.returncode != 0:
            return None
        
        stdout = result.stdout
        
        # Parse the results output from mutmut 2.x
        # Format example:
        # Survived (6)
        # ---- file.py (6) ----
        # 4, 9, 12, 16, 19, 21
        report = {}
        
        # Parse survived count from header like "Survived ... (6)"
        survived_header = re.search(r"Survived[^\(]*\((\d+)\)", stdout)
        if survived_header:
            report["survived"] = int(survived_header.group(1))
            # Extract individual IDs
            ids = re.findall(r"^[\d,\s]+$", stdout, re.MULTILINE)
            if ids:
                all_ids = []
                for id_line in ids:
                    all_ids.extend([int(x.strip()) for x in id_line.split(",") if x.strip().isdigit()])
                report["survived_mutant_ids"] = all_ids
        
        # Parse killed count if present
        killed_header = re.search(r"Killed[^\(]*\((\d+)\)", stdout)
        if killed_header:
            report["killed"] = int(killed_header.group(1))
        
        # Parse timeout count if present
        timeout_header = re.search(r"Timeout[^\(]*\((\d+)\)", stdout)
        if timeout_header:
            report["timeout"] = int(timeout_header.group(1))
        
        # Parse suspicious count if present
        suspicious_header = re.search(r"Suspicious[^\(]*\((\d+)\)", stdout)
        if suspicious_header:
            report["suspicious"] = int(suspicious_header.group(1))
        
        return report if report else None
        
    except Exception:
        return None


def get_surviving_mutants_details(cwd: Optional[str] = None) -> list[dict]:
    """
    Gets details about surviving mutants to understand test gaps.
    
    Args:
        cwd: Working directory
        
    Returns:
        List of dictionaries with mutant details
    """
    mutants = []
    
    try:
        # First get the list of survived mutant IDs
        result = subprocess.run(
            [sys.executable, "-m", "mutmut", "results"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30
        )
        
        # Extract survived mutant IDs
        survived_ids = re.findall(r"(?:Survived[:\s]+.*?)(\d+)", result.stdout, re.DOTALL)
        
        # Get details for each surviving mutant
        for mutant_id in survived_ids[:10]:  # Limit to first 10 for performance
            show_result = subprocess.run(
                [sys.executable, "-m", "mutmut", "show", mutant_id],
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=10
            )
            
            if show_result.returncode == 0:
                mutants.append({
                    "id": int(mutant_id),
                    "diff": show_result.stdout
                })
        
        return mutants
        
    except Exception:
        return []


def run_mutation_batch(
    test_configs: list[dict],
    cwd: Optional[str] = None,
    timeout_per_file: int = 300
) -> list[dict]:
    """
    Runs mutation testing for multiple source/test file pairs.
    
    Args:
        test_configs: List of dicts with 'source_file' and 'test_file' keys
        cwd: Working directory for running commands
        timeout_per_file: Timeout for each mutation run
        
    Returns:
        List of mutation testing results for each configuration
    """
    results = []
    for config in test_configs:
        result = run_mutation_testing(
            source_file=config["source_file"],
            test_file=config["test_file"],
            cwd=cwd,
            timeout=timeout_per_file
        )
        result["config"] = config
        results.append(result)
    return results


def get_mutation_summary(results: list[dict]) -> dict:
    """
    Generates a summary of mutation testing results.
    
    Args:
        results: List of mutation result dictionaries
        
    Returns:
        Summary dictionary with aggregate statistics
    """
    if not results:
        return {"error": "No results to summarize"}
    
    scores = [r["mutation_score"] for r in results if r["success"]]
    
    return {
        "total_files": len(results),
        "successful_runs": len(scores),
        "failed_runs": len(results) - len(scores),
        "average_mutation_score": sum(scores) / len(scores) if scores else 0,
        "min_mutation_score": min(scores) if scores else 0,
        "max_mutation_score": max(scores) if scores else 0,
        "total_killed": sum(r["killed"] for r in results),
        "total_survived": sum(r["survived"] for r in results),
        "total_mutants": sum(r["total_mutants"] for r in results),
    }


def print_mutation_report(result: dict, verbose: bool = True, show_survived: bool = False) -> None:
    """
    Prints a formatted mutation testing report to stdout.
    
    Args:
        result: Mutation testing result dictionary
        verbose: If True, prints detailed output
        show_survived: If True, shows details of surviving mutants
    """
    print("\n" + "=" * 60)
    print("MUTATION TESTING REPORT")
    print("=" * 60)
    
    if result.get("config"):
        print(f"Source: {result['config']['source_file']}")
        print(f"Tests:  {result['config']['test_file']}")
    
    print(f"\nMutation Score: {result['mutation_score']}%")
    print(f"Killed:    {result['killed']}")
    print(f"Survived:  {result['survived']}")
    print(f"Timeout:   {result['timeout']}")
    print(f"Suspicious: {result['suspicious']}")
    print(f"Skipped:   {result['skipped']}")
    print(f"Total:     {result['total_mutants']}")
    
    if show_survived and result.get("survived_mutant_ids"):
        print(f"\nSurviving mutant IDs: {result['survived_mutant_ids']}")
    
    if verbose and result.get("stdout"):
        print("\n" + "-" * 60)
        print("DETAILED OUTPUT:")
        print("-" * 60)
        print(result["stdout"])
    
    print("=" * 60 + "\n")


def generate_html_report(cwd: Optional[str] = None, output_file: str = "mutation_report.html") -> bool:
    """
    Generates an HTML report of the mutation testing results.
    
    Args:
        cwd: Working directory
        output_file: Output HTML file path
        
    Returns:
        True if report was generated successfully
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "mutmut", "html"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60
        )
        return result.returncode == 0
    except Exception:
        return False


# Main execution for standalone usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run mutation testing on source files")
    parser.add_argument("--source", "-s", required=True, help="Source file to mutate")
    parser.add_argument("--test", "-t", required=True, help="Test file to run")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--show-survived", action="store_true", help="Show surviving mutant details")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    result = run_mutation_testing(
        source_file=args.source,
        test_file=args.test,
        timeout=args.timeout
    )
    
    print_mutation_report(result, verbose=not args.quiet, show_survived=args.show_survived)
    
    if args.html:
        if generate_html_report():
            print("HTML report generated successfully!")
        else:
            print("Failed to generate HTML report.")
