import json
import os
import csv
from pathlib import Path
from datetime import datetime

def save_run_metrics(config_manager, results):
    # Extract timestamp from run_id (format: experiment_name_YYYY-MM-DDTHH:MM:SS)
    # The run_id contains experiment_name + '_' + timestamp
    run_id_parts = config_manager.run_id.rsplit('_', 1)
    timestamp = run_id_parts[1] if len(run_id_parts) > 1 else datetime.now().isoformat(timespec="seconds")

    metrics = {
        "run_id": config_manager.run_id,
        "experiment_name": config_manager.experiment_name,
        "timestamp": timestamp,
        "temperature": config_manager.get('llm', 'temperature'),
        "results": results,
    }

    # Save individual run file directly in results/ with run_id.json name
    file_path = os.path.join("results", f"{config_manager.run_id}.json")
    with open(file_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    # Append to a master CSV for easy Excel/Pandas analysis
    # _append_to_master_csv(metrics)
    
    print(f"📊 Results saved to {file_path}")