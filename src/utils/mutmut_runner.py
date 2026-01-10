import subprocess
import re
import sys
import shutil
from pathlib import Path
import os
import xml.etree.ElementTree as ET

def get_mutation_score_simple(
        source_file: str,       # file target da testare
        test_file: str          # file di test del file target
    ) -> dict:

    cache_path = Path(".mutmut-cache")
    if cache_path.exists():
        if cache_path.is_file(): cache_path.unlink()
        else: shutil.rmtree(cache_path)

    test_file_path = Path(test_file).resolve()
    test_dir = test_file_path.parent
    source_file_path = Path(source_file).resolve()
    project_root = Path.cwd().resolve()
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{project_root}:{env.get('PYTHONPATH', '')}"

    # --paths-to-mutate: limita i mutanti al solo file sorgente
    # --runner: specifica il comando per lanciare il test
    # --no-progress: evita barre di caricamento che rompono il parsing
    cmd = [
        sys.executable, "-m", "mutmut", "run",
        "--paths-to-mutate", str(source_file_path),
        "--tests-dir", str(test_dir),   # Dice a mutmut dove sono i test
        "--runner", f"pytest {test_file_path}", 
        "--no-progress",
        "--simple-output"
    ]
    
    try:
        # Timeout a 5 minuti per evitare loop infiniti generati dai mutanti
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            env=env
        )

        if result.returncode not in [0, 2]:
            # pass rate di base < 100
            return {
                "file": source_file_path.name,
                "mutation_score": 0,
                "success": False,
                "error": "Mutmut failed (code " + str(result.returncode) + "): " + result.stderr.strip()[-300:]
            }
        
        cmd_xml = [sys.executable, "-m", "mutmut", "junitxml"]
        
        xml_result = subprocess.run(
            cmd_xml,
            capture_output=True,
            text=True,
            env=env
        )
        
        if xml_result.returncode != 0:
             return {
                "file": source_file_path.name,
                "mutation_score": 0,
                "success": False,
                "error": "Failed to generate XML report"
            }

        # Parsing XML
        # Struttura tipica: <testsuite tests="10" failures="3" ...>
        # tests = totale mutanti
        # failures = mutanti sopravvissuti (survived)
        root = ET.fromstring(xml_result.stdout)
        
        total_mutants = int(root.attrib.get("tests", 0))
        survived = int(root.attrib.get("failures", 0)) # In mutation testing, failure del test = sopravvissuto
        killed = total_mutants - survived
        
        score = (killed / total_mutants * 100) if total_mutants > 0 else 0.0

        return {
            "file": source_file_path.name,
            "mutation_score": round(score, 2),
            "killed": killed,
            "survived": survived,
            "success": True
        }

    except subprocess.TimeoutExpired:
        print("Mutation testing timed out!")
        return {"file": Path(source_file).name, "mutation_score": 0, "success": False, "error": "Timeout"}
    except Exception as e:
        print(f"Error: {e}")
        return {"file": Path(source_file).name, "mutation_score": 0, "success": False, "error": str(e)}

# Esempio d'uso
# score = get_mutation_score_simple("data/input_code/library.py", "data/output_tests/agent_X/test_library.py")