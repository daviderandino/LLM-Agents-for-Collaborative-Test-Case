from pathlib import Path
from src.agents.multi_agent_competitive.multi_agent_competitive_runner import run_competitive_agents

if __name__ == '__main__':
    # Define the path using Path's / operator
    input_file_path = Path("data") / "input_code" / "hotel_reservation.py"

    # Pass the path as a string to the function,
    # since internal utilities often work with strings
    results = run_competitive_agents(
        input_file_path=str(input_file_path),
        planner_model='meta-llama/llama-4-scout-17b-16e-instruct',
        generator_model_1='meta-llama/llama-4-maverick-17b-128e-instruct',
        generator_model_2='openai/gpt-oss-20b',
        verbose=False
    )