import json
import os
import csv
from pathlib import Path

def save_run_metrics(config_manager, results):

    metrics = {
        "run_id": config_manager.run_id, # compaiono anche i nomi dei modelli
        "timestamp": config_manager.run_id, # Simplified
        "temperature": config_manager.get('llm', 'temperature'),
        "strict_imports": config_manager.get('agent', 'enforce_strict_imports'),
        "results": results,
        "total iterations": sum([res.get("metrics", {}).get("iterations", 0) for res in results]) if results else 0,
        "total_passed_tests": sum([res.get("metrics", {}).get("n_passed_tests", 0) for res in results]) if results else 0,
        "total_failed_tests": sum([res.get("metrics", {}).get("n_failed_tests", 0) for res in results]) if results else 0, 
        "total_tokens": sum([res.get("metrics", {}).get("total_tokens", 0) for res in results]) if results else 0,
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
        "temperature": metrics["temperature"],
        "passed_tests": metrics["total_passed_tests"],
        "failed_tests": metrics["total_failed_tests"],
        "iterations": metrics["total iterations"],
        "total_tokens": metrics["total_tokens"],
    }
    
    file_exists = csv_path.exists()
    
    with open(csv_path, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flat_metrics.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(flat_metrics)
    
    print(f"📝 Appended metrics to {csv_path}")