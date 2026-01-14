import json
import csv
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path.cwd()          # or Path("/path/to/project")
RESULTS_DIR = PROJECT_ROOT / "results"
OUT_CSV = PROJECT_ROOT / "all_metrics.csv"

COLUMNS = [
    "run_id",
    "experiment_name",
    "timestamp",
    "temperature",
    "file",
    "status",
    "coverage_percent",
    "n_passed_tests",
    "n_failed_tests",
    "iterations",
    "total_tokens",
    "mutation_score_percent",
    "mutation_killed",
    "mutation_survived",
]


def safe_get(d: Dict[str, Any], key: str, default=None):
    return d.get(key, default) if isinstance(d, dict) else default


def parse_metrics_json(path: Path) -> List[Dict[str, Any]]:
    """
    Returns a list of CSV rows (dict), one for each item in data["results"].
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    run_id = safe_get(data, "run_id")
    temperature = safe_get(data, "temperature")

    rows: List[Dict[str, Any]] = []
    for item in safe_get(data, "results", []) or []:
        metrics = safe_get(item, "metrics", {}) or {}

        row = {
            "run_id": run_id,
            "experiment_name": safe_get(data, "experiment_name"),
            "timestamp": safe_get(data, "timestamp"),
            "temperature": temperature,
            "file": safe_get(item, "file"),
            "status": safe_get(item, "status"),

            "coverage_percent": safe_get(metrics, "coverage_percent"),
            "n_passed_tests": safe_get(metrics, "n_passed_tests"),
            "n_failed_tests": safe_get(metrics, "n_failed_tests"),
            "iterations": safe_get(metrics, "iterations"),
            "total_tokens": safe_get(metrics, "total_tokens"),
            "mutation_score_percent": safe_get(metrics, "mutation_score_percent"),
            "mutation_killed": safe_get(metrics, "mutation_killed"),
            "mutation_survived": safe_get(metrics, "mutation_survived"),
        }
        rows.append(row)

    return rows


def main():
    if not RESULTS_DIR.exists():
        raise SystemExit(f"Directory not found: {RESULTS_DIR}")

    metrics_files = sorted(RESULTS_DIR.glob("*/metrics.json"))
    if not metrics_files:
        raise SystemExit(f"No files found in: {RESULTS_DIR}/*/metrics.json")

    all_rows: List[Dict[str, Any]] = []
    errors: List[str] = []

    for mp in metrics_files:
        try:
            all_rows.extend(parse_metrics_json(mp))
        except Exception as e:
            errors.append(f"{mp}: {type(e).__name__} - {e}")

    if not all_rows:
        raise SystemExit("No rows generated.")

    # Write CSV (UTF-8) to avoid Windows charmap issues
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"CSV successfully created: {OUT_CSV}")
    print(f"   Metrics files processed: {len(metrics_files)}")
    print(f"   Rows written: {len(all_rows)}")

    if errors:
        print("\nErrors while processing some metrics.json files:")
        for err in errors:
            print(" -", err)


if __name__ == "__main__":
    main()
