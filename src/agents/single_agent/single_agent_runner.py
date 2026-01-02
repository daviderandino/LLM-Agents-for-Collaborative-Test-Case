from src.agents.single_agent.SingleAgentChain import SingleAgentChain
from src.agents.llm_factory import get_llm

def run_single_agent(
        input_file_path,
        output_dir,
        model,
        temperature=0
    ): 
    # Pass temperature to factory
    llm = get_llm(
        provider='groq',
        model_name=model,
        temperature=temperature
    )
    
    agent = SingleAgentChain(
        input_file_path,
        output_dir,
        llm
    )

    final_state = agent.invoke()

    return {
        "coverage_percent": final_state.get("coverage_percent", 0), 
        "n_passed_tests": final_state.get("n_passed_tests", 0),
        "n_failed_tests": final_state.get("n_failed_tests", 0),
        "iterations": final_state.get("iterations", 0),
        "total_tokens": final_state.get("total_tokens", 0)
    }