import json
import pandas as pd
from pathlib import Path
from src.utils.mutmut_runner import get_mutation_score_simple

PROJECT_ROOT = Path.cwd()
RESULTS_DIR = PROJECT_ROOT / "results"
INPUT_CODE_DIR = PROJECT_ROOT / "data" / "input_code"
OUTPUT_TESTS_DIR = PROJECT_ROOT / "data" / "output_tests"

def evaluate_experiment(experiment_name: str):
    """
    Analizza un esperimento specifico, calcola le metriche mancanti (Mutation Score)
    e ritorna una tabella Pandas con le info dell'esperimento.
    """
    
    metrics_path = RESULTS_DIR / experiment_name / "metrics.json"
    
    if not metrics_path.exists():
        print(f"❌ Errore: File non trovato: {metrics_path}")
        return

    try:
        with open(metrics_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Errore: Il file JSON è corrotto.")
        return

    rows = []

    # itero su ogni file processato nell'esperimento
    for result in data.get("results", []):
        filename = result.get("file")
        metrics = result.get("metrics", {})
        
        coverage = metrics.get("coverage_percent", 0)
        n_passed = metrics.get("n_passed_tests", 0)
        n_failed = metrics.get("n_failed_tests", 0)
        tokens = metrics.get("total_tokens", 0)
        
        # --- CALCOLO PASS RATE ---
        total_tests = n_passed + n_failed
        pass_rate = (n_passed / total_tests * 100) if total_tests > 0 else 0.0
        
        # --- CALCOLO MUTATION SCORE ---
        mutation_score = 0.0
        mutation_note = "" # per indicare se è stato skippato
        
        # Eseguiamo Mutmut SOLO se i test passano tutti
        if n_failed == 0 and n_passed > 0:
            source_file = (INPUT_CODE_DIR / filename).resolve()
            test_file = (OUTPUT_TESTS_DIR / experiment_name / f"test_{filename}").resolve()
            
            if test_file.exists():
                # Chiamata alla funzione nel tuo file esterno
                mut_res = get_mutation_score_simple(str(source_file), str(test_file))
    
                if mut_res["success"]:
                    mutation_score = mut_res["mutation_score"]
                else:
                    mutation_note = "Error" # Timeout o errore interno
            else:
                mutation_note = "No File" # File di test non trovato su disco
                
        elif n_failed > 0:
            mutation_note = "Fail" # Skippato perché i test falliscono
            # mutation_score resta 0
        else:
            mutation_note = "No Tests" # 0 test generati
        
        rows.append({
            "File": filename,
            "Coverage (%)": coverage,
            "Pass Rate (%)": round(pass_rate, 2),
            "Mutation Score (%)": mutation_score,
            "Tokens": tokens,
            "Note": mutation_note
        })

    df = pd.DataFrame(rows)
    
    if df.empty:
        print("Nessun risultato trovato.")
        return

    # Media su TUTTI i file target.
    # Nota: per la media mutation score, includiamo anche gli zeri (penalizzando chi fallisce i test)
    avg_row = {
        "File": "MEAN",
        "Coverage (%)": round(df["Coverage (%)"].mean(), 2),
        "Pass Rate (%)": round(df["Pass Rate (%)"].mean(), 2),
        "Mutation Score (%)": round(df["Mutation Score (%)"].mean(), 2),
        "Tokens": df["Tokens"].mean(),
        "Note": ""
    }
    
    df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    return df
