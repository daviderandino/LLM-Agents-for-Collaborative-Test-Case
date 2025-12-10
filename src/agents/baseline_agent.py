import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate # permette di dividere system prompt e user message
#from langchain_core.prompts import PromptTemplate # se vogliamo un unico raw message


# ========== SETUP ENVIRONMENT & PATHS ==========
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

if project_root not in sys.path:
    sys.path.append(project_root)

dotenv_path = os.path.join(project_root, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# ========== INITIALIZE LLM ==========
from llm_factory import get_llm
llm = get_llm()
#llm = get_llm(provider="groq", model_name="llama-3.1-8b-instant", temperature=0)


# ========== HELPER FUNCTIONS ==========
def clean_code_output(text: str) -> str:
    """
    This function uses a regex to extract only what is
    between the backticks ```python ... ``` and discards the rest..
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n", 1)
        if len(lines) > 1:
            cleaned = lines[1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("\n", 1)[0]
    return cleaned.strip()


def run_baseline_agent(input_path: str, output_path: str):
    
    # Read the Input Code, per cui vanno generati i test
    full_input_path = os.path.join(project_root, input_path)
    if not os.path.exists(full_input_path):
        print(f"Error: Input file not found at {full_input_path}")
        return

    with open(full_input_path, "r") as f:
        code_under_test = f.read()

    # Calculate the module name for import
    # Example: from "data/input_code/bank_account.py" -> "input_code.bank_account"
    file_name = os.path.basename(input_path)       # bank_account.py
    base_name = os.path.splitext(file_name)[0]     # bank_account
    # We assume files are always in 'input_code'
    target_module = f"data.input_code.{base_name}"

    # Definiamo il template: di fatto è il prompt con placeholders, quando li riempiremo sarà
    # più corretto chiamarlo prompt.
    # Attenzione!!! agli spazi/tabulazioni quando si usa """ ... """ in Python.
    template = ChatPromptTemplate.from_messages([
        (
            "system", 
"""You are an expert Software Engineer in Test (SDET).
Your goal is to write a high-quality unit test suite using 'pytest' for the provided Python code.

While generating the output, you have to follow those three instructions:
- **IMPORTANT**: Import the class or functions to test specifically from the module `{target_module}`. 
    (Example: `from {target_module} import ...`)
- Write test cases for success scenarios, edge cases, and error handling.
- Output ONLY the raw Python code. Do not include markdown formatting or explanations."""
        ),
        (
            "human", 
"""Write a unit test suite for the Python code below:

{code_under_test}"""
        ),
    ])

    # creiamo una catena (tramite sintassi speciale di LangChain "|": si prende il template
    # e lo si collega in input all'LLM) definita come oggetto 'RunnableSequence'
    chain = template | llm # -> logica lazy: non è ancora stata chiamata l'API di Groq ma si è solo definita la "ricetta" che definisce la chain
    
    # definiamo come riempire i placeholders del template
    chain_input = {
        "code_under_test": code_under_test, 
        "target_module": target_module
    }
    # facciamo partire la catena. invoke() si metterà in attesa della risposta, che sarà un oggetto 'AIMessage' 
    response = chain.invoke(chain_input)

    # Nota: in generale, l'input che prende .invoke() viene sempre dato al primo componente della
    # pipe/catena, dunque deve rispettare, appunto, il formato di input che deve prendere quel
    # componente. Dipende tutto da chi è il primo anello della catena. Nel nostro caso, il primo
    # componente è un ChatPromptTemplate che esige come input un dizionario che contenga il valore
    # da assegnare ai placeholder.
    
    generated_text = response.content if hasattr(response, 'content') else str(response) # estrae il contenuto della risposta, gestendo caso di errore
    
    final_code = clean_code_output(generated_text)
    
    full_output_path = os.path.join(project_root, output_path)
    os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
    
    with open(full_output_path, "w") as f:
        f.write(final_code)
        
    print(f"Success! Tests generated and saved to: {output_path}")


if __name__ == "__main__":
    INPUT_FILE = "data/input_code/bank_account.py"
    OUTPUT_FILE = "data/output_tests/baseline/test_bank_account.py"
    
    run_baseline_agent(INPUT_FILE, OUTPUT_FILE)
