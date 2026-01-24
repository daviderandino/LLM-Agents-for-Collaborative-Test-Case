from src.agents.multi_agent_competitive.MultiAgentCompetitiveGraph import MultiAgentCompetitiveGraph
from src.agents.llm_factory import get_llm

def run_competitive_agents(
        input_file_path, 
        output_dir,
        planner_model, 
        generator_model_1, 
        generator_model_2, 
        planner_temperature=0,
        generator_1_temperature=0,
        generator_2_temperature=0,
        verbose=False
    ): 

    llm_planner = get_llm(
        provider='groq',
        model_name=planner_model, 
        temperature=planner_temperature
    )
    llm_generator_1 = get_llm(
        provider='groq', 
        model_name=generator_model_1, 
        temperature=generator_1_temperature
    )
    llm_generator_2 = get_llm(
        provider='groq', 
        model_name=generator_model_2, 
        temperature=generator_2_temperature
    )

    agents = MultiAgentCompetitiveGraph(
        input_file_path,
        output_dir,
        llm_planner,
        llm_generator_1,
        llm_generator_2,
        verbose
    )

    final_state = agents.invoke()

    return {
        "coverage_percent": final_state.get("coverage_percent", 0), 
        "n_passed_tests": final_state.get("n_passed_tests", 0),
        "n_failed_tests": final_state.get("n_failed_tests", 0),
        "failed_tests_infos": final_state.get("failed_tests_infos", ""),
        "iterations": final_state.get("iterations", 0),
        "cost": final_state.get("cost", 0),
        "total_tokens": final_state.get("total_tokens", 0),
        "mutation_score_percent": final_state.get("mutation_score_percent", None)
    }