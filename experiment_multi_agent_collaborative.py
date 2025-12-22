from pathlib import Path
from src.agents.multi_agent_collaborative.multi_agent_collaborative_runner import run_collaborative_agents

if __name__ == '__main__':
    # Define the path using Path's / operator
    input_file_path = Path("data") / "input_code" / "complex_logic.py"

    # Pass the path as a string to the function,
    # since internal utilities often work with strings
    results = run_collaborative_agents(
        input_file_path=str(input_file_path),
        planner_model='meta-llama/llama-4-scout-17b-16e-instruct',
        generator_model='meta-llama/llama-4-maverick-17b-128e-instruct',
        verbose= True
    )