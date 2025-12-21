from pathlib import Path
from src.agents.multi_agent_collaborative.multi_agent_collaborative_runner import run_collaborative_agents
from tqdm import tqdm

if __name__ == '__main__':
    # Configuration of paths and models
    input_dir = Path("data") / "input_code"
    planner_model = 'openai/gpt-oss-20b'
    generator_model = 'openai/gpt-oss-20b'

    # Retrieve all .py files excluding __init__.py
    files_to_test = [
        f for f in input_dir.glob("*.py") 
        if f.name != '__init__.py'
    ]

    print(f"Found {len(files_to_test)} files for the Multi-Agent experiment.\n")

    # Iterative loop over each file in the dataset
    for file_path in tqdm(files_to_test, desc="Collaborative generation"):
        
        print(f"\n--- Starting Collaboration: {file_path.name} ---")
        
        try:
            # Pass the path as a string to the runner function
            results = run_collaborative_agents(
                str(file_path),
                planner_model=planner_model,
                generator_model=generator_model
            )
            # Note: final results (coverage, iterations) are saved
            # in the final state returned by run_collaborative_agents.
            
        except Exception as e:
            print(f"Critical error during execution on {file_path.name}: {e}")

    print("\nMulti-Agent experiment completed for all files.")