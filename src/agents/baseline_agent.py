import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate


# --- 1. SETUP ENVIRONMENT & PATHS ---

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

if project_root not in sys.path:
    sys.path.append(project_root)

dotenv_path = os.path.join(project_root, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from llm_factory import get_llm


# --- 2. INITIALIZE LLM ---

#llm = get_llm(provider="groq", model_name="llama-3.1-8b-instant", temperature=0)
llm = get_llm()

# --- 3. HELPER FUNCTIONS ---

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
    
    # 1. Read the Input Code, per cui vanno generati i test
    full_input_path = os.path.join(project_root, input_path)
    if not os.path.exists(full_input_path):
        print(f"Error: Input file not found at {full_input_path}")
        return

    with open(full_input_path, "r") as f:
        code_under_test = f.read()

    # 2. Calculate the module name for import
    # Example: from "data/input_code/bank_account.py" -> "input_code.bank_account"
    file_name = os.path.basename(input_path)       # bank_account.py
    base_name = os.path.splitext(file_name)[0]     # bank_account
    # We assume files are always in 'input_code'
    target_module = f"data.input_code.{base_name}"

    # 3. Define the Prompt
    # Attenzione agli spazi/tabulazioni quando si usa """ ... """ in Python.
    template = """
You are an expert Software Engineer in Test (SDET).
    
Your goal is to write a high-quality unit test suite using 'pytest' for the target Python code provided below.
    
Instructions:
- **IMPORTANT**: Import the class or functions to test specifically from the module `{target_module}`. 
    (Example: `from {target_module} import ...`)
- Write test cases for success scenarios, edge cases, and error handling.
- Output ONLY the raw Python code. Do not include markdown formatting or explanations.
    
Target Python code:
{code} 
"""
    
    prompt = PromptTemplate(
        input_variables=["code", "target_module"],
        template=template,
    )

    # 4. Generate Tests
    print(f"Generating tests for {input_path} (Module: {target_module})...")
    chain = prompt | llm  # Take the prompt output and pass it as input to the LLM
    
    # Pass both the code and module name to the prompt.
    # LangChain take the dictionary and fill the PromptTemplate
    # And it calls the API (Groq server)
    response = chain.invoke({
        "code": code_under_test, 
        "target_module": target_module
    })
    
    generated_text = response.content if hasattr(response, 'content') else str(response)
    
    # 5. Save Output
    final_code = clean_code_output(generated_text)
    
    full_output_path = os.path.join(project_root, output_path)
    os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
    
    with open(full_output_path, "w") as f:
        f.write(final_code)
        
    print(f"Success! Tests saved to: {output_path}")

# --- 4. EXECUTION ---

if __name__ == "__main__":
    INPUT_FILE = "data/input_code/bank_account.py"
    OUTPUT_FILE = "data/output_tests/baseline/test_bank_account.py"
    
    run_baseline_agent(INPUT_FILE, OUTPUT_FILE)