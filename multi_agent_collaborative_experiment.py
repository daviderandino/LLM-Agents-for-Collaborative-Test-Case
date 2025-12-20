from src.agents.multi_agent_collaborative.multi_agent_collaborative_runner import run_collaborative_agents
import os


if __name__ == '__main__':

    input_file_path = os.path.join("data", "input_code", "library.py")

    results = run_collaborative_agents(
        input_file_path,
        planner_model='openai/gpt-oss-20b',
        generator_model='openai/gpt-oss-20b'
    )