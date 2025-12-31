import json
import os
import csv
from pathlib import Path

def save_run_metrics(config_manager, final_coverage, tests_passed, tests_failed, total_cost, iterations, total_tokens=0):
    metrics = {
        "run_id": config_manager.run_id,
        "timestamp": config_manager.run_id, # Simplified
        "model": config_manager.get('llm', 'model'),
        "temperature": config_manager.get('llm', 'temperature'),
        "strict_imports": config_manager.get('agent', 'enforce_strict_imports'),
        "results": {
            "coverage_pct": final_coverage,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "iterations": iterations,
            "total_tokens": total_tokens
        },
        "cost_estimate": total_cost
    }

    # Save individual run file
    file_path = os.path.join(config_manager.results_dir, "metrics.json")
    with open(file_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    # Append to a master CSV for easy Excel/Pandas analysis
    _append_to_master_csv(metrics)
    
    print(f"📊 Results saved to {file_path}")

def _append_to_master_csv(metrics):
    # Logic to append a single line to results/master_log.csv
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_path = results_dir / "master_log.csv"
    
    # Flatten metrics for CSV
    flat_metrics = {
        "run_id": metrics["run_id"],
        "timestamp": metrics["timestamp"],
        "model": metrics["model"],
        "temperature": metrics["temperature"],
        "strict_imports": metrics["strict_imports"],
        "coverage_pct": metrics["results"]["coverage_pct"],
        "tests_passed": metrics["results"]["tests_passed"],
        "tests_failed": metrics["results"]["tests_failed"],
        "iterations": metrics["results"]["iterations"],
        "total_tokens": metrics["results"].get("total_tokens", 0),
        "cost_estimate": metrics["cost_estimate"]
    }
    
    file_exists = csv_path.exists()
    
    with open(csv_path, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flat_metrics.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(flat_metrics)
    
    print(f"📝 Appended metrics to {csv_path}")