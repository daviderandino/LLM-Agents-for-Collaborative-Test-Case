from src.agents.multi_agent_collaborative_natural.MultiAgentCollaborativeGraph import MultiAgentCollaborativeGraph 
from src.agents.llm_factory import get_llm

def run_collaborative_agents(
        input_file_path, 
        output_dir,
        planner_model, 
        generator_model, 
        planner_temperature=0,
        generator_temperature=0,
        verbose=False,
        max_iterations=10
    ): 
    
    llm_planner = get_llm(
        provider='groq', 
        model_name=planner_model, 
        temperature=planner_temperature
    )
    llm_generator = get_llm(
        provider='groq', 
        model_name=generator_model, 
        temperature=generator_temperature
    )

    agents = MultiAgentCollaborativeGraph(
        input_file_path,
        output_dir,
        llm_planner,
        llm_generator,
        verbose,
        max_iterations
    )

    final_state = agents.invoke()

    return {
        "coverage_percent": final_state.get("coverage_percent", 0), 
        "n_passed_tests": final_state.get("n_passed_tests", 0),
        "n_failed_tests": final_state.get("n_failed_tests", 0),
        "failed_tests_infos": final_state.get("failed_tests_infos", ""),
        "iterations": final_state.get("iterations", 0),
        "total_tokens": final_state.get("total_tokens", 0),
        "mutation_score_percent": final_state.get("mutation_score_percent", None)
    }