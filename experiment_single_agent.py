from pathlib import Path
from src.agents.single_agent.single_agent_runner import run_single_agent

if __name__ == '__main__':
    # Constructing the path with pathlib
    input_file_path = Path("data") / "input_code" / "bank_account.py"

    # Running the agent by converting the path to a string
    results = run_single_agent(
        input_file_path=str(input_file_path),
        model='openai/gpt-oss-20b',
    )