from src.agents.single_agent.single_agent_runner import run_single_agent
import os


if __name__ == '__main__':

    input_file_path = os.path.join("data", "input_code", "bank_account.py")

    results = run_single_agent(
        input_file_path,
        model='openai/gpt-oss-20b',
    )