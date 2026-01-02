from src.agents.multi_agent_collaborative.MultiAgentCollaborativeGraph import MultiAgentCollaborativeGraph 
from src.agents.llm_factory import get_llm

def run_collaborative_agents(
        input_file_path, 
        output_dir,
        planner_model, 
        generator_model, 
        temperature=0, 
        verbose=False
    ): 
    
    llm_planner = get_llm(
        provider='groq', 
        model_name=planner_model, 
        temperature=temperature
    )
    llm_generator = get_llm(
        provider='groq', 
        model_name=generator_model, 
        temperature=temperature
    )

    agents = MultiAgentCollaborativeGraph(
        input_file_path,
        output_dir,
        llm_planner,
        llm_generator,
        verbose
    )

    final_state = agents.invoke()

    return {
        "coverage_percent": final_state.get("coverage_percent", 0), 
        "n_passed_tests": final_state.get("n_passed_tests", 0),
        "n_failed_tests": final_state.get("n_failed_tests", 0),
        "iterations": final_state.get("iterations", 0),
        "total_tokens": final_state.get("total_tokens", 0)
    }