from pathlib import Path
from src.agents.multi_agent_collaborative.multi_agent_collaborative_runner import run_collaborative_agents

if __name__ == '__main__':
    # Define the path using Path's / operator
    input_file_path = Path("data") / "input_code" / "library.py"

    # Pass the path as a string to the function,
    # since internal utilities often work with strings
    results = run_collaborative_agents(
        input_file_path=str(input_file_path),
        planner_model='openai/gpt-oss-20b',
        generator_model='openai/gpt-oss-20b'
    )