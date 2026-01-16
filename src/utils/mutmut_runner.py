import subprocess
import sys
from pathlib import Path
import os
import json
from typing import Dict, Optional


def get_mutation_metrics(source_file_path: str, test_file_path: str) -> Optional[Dict]:
    """
    Calcola le metriche di mutation testing usando mutmut.
    
    Args:
        source_file_path: Path del file sorgente da testare
        test_file_path: Path del file di test specifico
        
    Returns:
        Dict con mutation_score_percent, mutation_killed, mutation_survived oppure None se fallisce
    """
    source_file = Path(source_file_path).resolve()
    test_file = Path(test_file_path).resolve()
    test_dir = test_file.parent
    
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{Path.cwd()}:{env.get('PYTHONPATH', '')}"

    cmd = [
        sys.executable, "-m", "mutmut", "run",
        "--paths-to-mutate", str(source_file),
        "--tests-dir", str(test_dir),
        "--runner", f"pytest {test_file}",
        "--no-progress"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
        
        if result.returncode not in [0, 2]:
            return None
        
        # Conta i mutanti killed usando mutmut result-ids
        killed_cmd = [sys.executable, "-m", "mutmut", "result-ids", "killed"]
        killed_output = subprocess.run(killed_cmd, capture_output=True, text=True, env=env)
        
        # Conta i mutanti survived
        survived_cmd = [sys.executable, "-m", "mutmut", "result-ids", "survived"]
        survived_output = subprocess.run(survived_cmd, capture_output=True, text=True, env=env)
        
        if killed_output.returncode != 0 or survived_output.returncode != 0:
            return None
        
        # Conta il numero di IDs (separati da spazi)
        killed = len(killed_output.stdout.strip().split()) if killed_output.stdout.strip() else 0
        survived = len(survived_output.stdout.strip().split()) if survived_output.stdout.strip() else 0
        total = killed + survived
        
        score = (killed / total * 100) if total > 0 else 0.0
        
        return {
            "mutation_score_percent": round(score, 2),
            "mutation_killed": killed,
            "mutation_survived": survived
        }
    
    except (subprocess.TimeoutExpired, Exception):
        return None
    