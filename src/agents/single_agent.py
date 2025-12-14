import os
import sys
import subprocess
import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Otteniamo la cartella corrente (src/agents)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Risaliamo di due livelli per trovare la root (LLM-AGENTS-...)
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

# Aggiungiamo la root al system path così Python trova i moduli ovunque
if project_root not in sys.path:
    sys.path.append(project_root)

# Carichiamo il .env dalla root
load_dotenv(os.path.join(project_root, '.env'))

# --- IMPORT LOCALI ---
# Essendo nella stessa cartella (src/agents), questi import funzionano direttamente
try:
    from llm_factory import get_llm
    from simple_llm_chain import clean_code_output
except ImportError:
    # Fallback se eseguiamo lo script in modo diverso (es. come modulo)
    from src.agents.llm_factory import get_llm
    from src.agents.simple_llm_chain import clean_code_output


# --- CONFIGURAZIONE LLM ---
# Usiamo temperature bassa per avere codice più deterministico
llm = get_llm(temperature=0.1)

# --- 1. DEFINIZIONE DELLO STATO (The Agent's Memory) ---
class AgentState(TypedDict):
    input_file_path: str      # Path del file originale
    target_module: str        # Nome del modulo per l'import (es: data.input_code.bank)
    code_under_test: str      # Contenuto del codice sorgente
    
    test_plan: str            # Il piano generato (to-do list)
    generated_tests: str      # Il codice pytest generato
    
    test_output: str          # Output della console di pytest
    coverage_percent: int     # Percentuale di coverage raggiunta (0-100)
    error_occurred: bool      # Flag: ci sono stati errori di sintassi/runtime?
    
    iterations: int           # Contatore per evitare loop infiniti


# --- 2. DEFINIZIONE DEI NODI ---
def plan_node(state: AgentState):
    """
    Analizza il codice e crea un piano di test.
    Se arriva da un fallimento (retry), legge l'errore precedente.
    """
    print(f"\n--- STEP 1: PLANNING (Iteration {state['iterations'] + 1}) ---")
    
    # Costruiamo il contesto: è il primo giro o stiamo correggendo errori?
    context = ""
    if state.get("test_output"):
        context = f"""
        WARNING: PREVIOUS TEST EXECUTION FAILED or HAD LOW COVERAGE.
        Current Coverage: {state.get('coverage_percent', 0)}%
        
        Previous Output/Errors:
        {state['test_output']}
        
        INSTRUCTION: Refine the plan to specifically fix these errors and cover missing lines.
        """

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a QA Lead. Analyze the code and create a detailed step-by-step testing plan."),
        (
            "human",
            """
            Code to test:
            {code}
            
            {context}
            
            Return ONLY the textual plan (a concise TODO list of scenarios to test).
            """
        )
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "code": state["code_under_test"],
        "context": context
    })
    
    # Aggiorniamo lo stato con il nuovo piano e incrementiamo il contatore
    return {"test_plan": response.content, "iterations": state["iterations"] + 1}


def generation_node(state: AgentState):
    """
    Scrive il codice Python dei test basandosi sul piano.
    """
    print("--- STEP 2: GENERATING TESTS ---")
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a Python Testing Expert (pytest).
            Write a complete test suite based on the plan provided.
            
            CRITICAL RULES:
            1. **ALWAYS start the file with `import pytest`**. This is mandatory.
            2. Import the module exactly using: `from {target_module} import ...`
            3. Use standard `pytest` syntax (fixtures, raises, marks).
            4. Output ONLY raw python code inside backticks (```python ... ```).
            5. Do NOT include explanations.
            6. Just output the code block, nothing else.
            7. **NO TEXT AFTER THE CODE**. Do not write "Here is the code" or "This covers X".
            """
        ),
        (
            "human",
            """
            Plan:
            {plan}
            
            Original Code:
            {code}
            
            Generate the full `test_suite.py` file content.
            """
        )
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "target_module": state["target_module"],
        "plan": state["test_plan"],
        "code": state["code_under_test"]
    })
    
    # Puliamo l'output per avere solo codice
    cleaned_code = clean_code_output(response.content)
    
    return {"generated_tests": cleaned_code}


def execution_node(state: AgentState):
    """
    Salva il file, esegue pytest e legge la coverage.
    """
    print("--- STEP 3: EXECUTING PYTEST ---")
    
    # 1. Salviamo il file di test temporaneo
    # Nota: Lo salviamo nella root per semplicità di import
    test_filename = "temp_test_execution.py"
    test_file_path = os.path.join(project_root, test_filename)
    
    with open(test_filename, "w") as f:
        f.write(state["generated_tests"])
    
    # 2. Eseguiamo Pytest
    cmd = [
        "pytest", 
        test_filename, 
        f"--cov={state['target_module']}",  # <--- MODIFICA QUI: Usa il nome del modulo (con i punti)
        "--cov-report=term-missing"
    ]
    
    try:
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=project_root, 
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        # Se il returncode non è 0, pytest ha fallito (test rossi o errore sintassi)
        is_error = result.returncode != 0

        # --- DEBUG PRINT ---
        if is_error:
            print("\n!!! PYTEST FAILURE OUTPUT !!!")
            # Stampiamo solo le ultime 10 righe dell'errore per non intasare la console
            print('\n'.join(output.splitlines()[-15:]))
            print("!!! END FAILURE OUTPUT !!!\n")

    except Exception as e:
        output = str(e)
        is_error = True
        print(f"EXCEPTION DURING EXECUTION: {e}")

    # 3. Parsing della Coverage
    # Cerchiamo la riga finale di report coverage, es: "TOTAL 20 5 75%"
    # Regex cerca un numero percentuale alla fine della riga che inizia con TOTAL
    # Nota: l'output varia leggermente in base alla versione, questa regex è generica
    cov_match = re.search(r"TOTAL.*?(\d+)%", output)
    coverage = int(cov_match.group(1)) if cov_match else 0
    
    print(f"--- EXECUTION RESULT: Errors={is_error}, Coverage={coverage}% ---")
    
    # (Opzionale) Rimuovi il file temporaneo se vuoi pulizia
    if os.path.exists(test_file_path):
        os.remove(test_file_path) 

    return {
        "test_output": output,
        "coverage_percent": coverage,
        "error_occurred": is_error
    }


# --- 3. LOGICA CONDIZIONALE (ROUTER) ---
def router(state: AgentState):
    """
    Decide se finire o tornare indietro.
    """
    # Limite di sicurezza per evitare loop infiniti (e costi API)
    MAX_ITERATIONS = 5
    if state["iterations"] >= MAX_ITERATIONS:
        print(f"--- STOPPING: Reached max iterations ({MAX_ITERATIONS}) ---")
        return "end"
    
    # Se i test passano (no errori) e la coverage è 100%, abbiamo finito
    if not state["error_occurred"] and state["coverage_percent"] == 100:
        print("--- SUCCESS: 100% Coverage achieved! ---")
        return "end"
    
    # Altrimenti, rigeneriamo il piano
    print("--- DECISION: Re-planning (Low coverage or Errors) ---")
    return "re-plan"


# --- 4. COSTRUZIONE DEL GRAFO ---
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Aggiungi nodi
    workflow.add_node("planner", plan_node)
    workflow.add_node("generator", generation_node)
    workflow.add_node("executor", execution_node)
    
    # Entry point
    workflow.set_entry_point("planner")
    
    # Archi normali
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", "executor")
    
    # Arco condizionale
    workflow.add_conditional_edges(
        "executor",
        router,
        {
            "re-plan": "planner",
            "end": END
        }
    )
    
    return workflow.compile()


# --- 5. MAIN ---
if __name__ == "__main__":
    
    # ESEMPIO DI SETUP
    # Assicurati che questo file esista!
    input_file_rel = "data/input_code/bank_account.py"
    input_file_abs = os.path.join(project_root, input_file_rel)
    
    # Il nome del modulo Python per l'import statement
    # Se il file è in data/input_code/bank_account.py, l'import è data.input_code.bank_account
    target_module = "data.input_code.bank_account"
    
    # Verifica esistenza file input
    if not os.path.exists(input_file_abs):
        print(f"ERRORE: File non trovato: {input_file_abs}")
        exit()

    # Leggiamo il codice
    with open(input_file_abs, "r") as f:
        code = f.read()
        
    # Stato iniziale
    initial_state = {
        "input_file_path": input_file_abs,
        "target_module": target_module,
        "code_under_test": code,
        "test_plan": "",
        "generated_tests": "",
        "test_output": "",
        "coverage_percent": 0,
        "error_occurred": False,
        "iterations": 0
    }
    
    print(f"Starting Agent for {input_file_rel}...")
    
    # Avvio del grafo
    app = build_graph()
    final_state = app.invoke(initial_state)
    
    # Salvataggio in data/output_tests
    output_filename = f"test_{os.path.basename(input_file_rel)}"
    output_path = os.path.join(project_root, "data/output_tests", output_filename)
    
    # Assicurati che la cartella esista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(final_state["generated_tests"])
        
    print(f"\nWorkflow Finished.")
    print(f"Final Coverage: {final_state['coverage_percent']}%")
    print(f"Tests saved to: {output_path}")
