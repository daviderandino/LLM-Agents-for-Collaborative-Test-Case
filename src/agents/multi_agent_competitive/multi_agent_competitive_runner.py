from src.agents.multi_agent_competitive.MultiAgentCompetitiveGraph import MultiAgentCompetitiveGraph
from src.agents.llm_factory import get_llm

def run_competitive_agents(input_file_path, planner_model, generator_model_1, generator_model_2, verbose): 

    llm_planner = get_llm(provider='groq', model_name=planner_model)
    llm_generator_1 = get_llm(provider='groq', model_name=generator_model_1)
    llm_generator_2 = get_llm(provider='groq', model_name=generator_model_2)

    agents = MultiAgentCompetitiveGraph(
        input_file_path,
        llm_planner,
        llm_generator_1,
        llm_generator_2,
        verbose
    )

    final_state = agents.invoke()

    ### è da estrarre coverage, iterations etc e ritornarle se si vogliono fare statistiche nell'esperimento
    return {
        "...": 0
    }