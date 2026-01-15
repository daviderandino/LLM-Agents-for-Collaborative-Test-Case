import subprocess
import sys
import shutil
from pathlib import Path
import os
import xml.etree.ElementTree as ET
from typing import Optional


def get_mutation_score(source_file: str, test_file: str) -> Optional[float]:
    """
    Esegue mutmut sul file sorgente.
    Ritorna il punteggio (0-100) se l'esecuzione ha successo.
    Ritorna None se mutmut fallisce (es. clean run fallita, errori di sintassi).
    """

    cache_path = Path(".mutmut-cache")
    if cache_path.exists():
        if cache_path.is_file():
            cache_path.unlink()
        else:
            shutil.rmtree(cache_path)

    test_file_path = Path(test_file).resolve()
    test_dir = test_file_path.parent
    source_file_path = Path(source_file).resolve()
    project_root = Path.cwd().resolve()
    
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    env["PYTHONPATH"] = f"{project_root}{os.pathsep}{current_pythonpath}"

    cmd = [
        sys.executable, "-m", "mutmut", "run",
        "--paths-to-mutate", str(source_file_path),
        "--tests-dir", str(test_dir),
        "--runner", f"{sys.executable} -m pytest {test_file_path}", 
        "--no-progress",
        "--simple-output"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            env=env
        )

        # Se il return code non è 0 (successo totale) o 2 (mutanti trovati/sopravvissuti),
        # significa che mutmut è crashato (es. 'Clean run failed' se i test base non passano).
        if result.returncode not in [0, 2]:
            return None
        
        # report XML
        cmd_xml = [sys.executable, "-m", "mutmut", "junitxml"]
        xml_result = subprocess.run(
            cmd_xml,
            capture_output=True,
            text=True,
            env=env
        )
        
        if xml_result.returncode != 0:
             return None

        root = ET.fromstring(xml_result.stdout)
        total_mutants = int(root.attrib.get("tests", 0))
        survived = int(root.attrib.get("failures", 0))
        killed = total_mutants - survived
        
        if total_mutants == 0:
            return 0.0
            
        score = (killed / total_mutants) * 100
        return round(score, 2)

    except (subprocess.TimeoutExpired, Exception):
        # In caso di timeout o eccezioni impreviste, ritorna
        return None
    