from pathlib import Path
from src.agents.single_agent.single_agent_runner import run_single_agent
from tqdm import tqdm

if __name__ == '__main__':
    # Define the folder path as a Path object
    # The / operator safely joins paths for each operating system
    input_dir = Path("data") / "input_code"
    model_name = 'openai/gpt-oss-20b'

    # .glob("*.py") finds all python files in the folder
    # We filter by excluding __init__.py by checking the .name attribute
    files_to_test = [
        f for f in input_dir.glob("*.py") 
        if f.name != '__init__.py'
    ]

    print(f"Found {len(files_to_test)} files to process.\n")

    # Loop through all Path objects found
    for file_path in tqdm(files_to_test, desc="Test generation"):
        
        # .name returns only the filename (e.g: "bank_account.py")
        print(f"\n--- Processing: {file_path.name} ---")
        
        try:
            # Convert the Path object to string for the run_single_agent function
            results = run_single_agent(
                str(file_path),
                model=model_name,
            )
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    print("\nProcess completed for all files.")