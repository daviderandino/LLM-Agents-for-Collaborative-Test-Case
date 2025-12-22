from src.agents.multi_agent_collaborative.MultiAgentCollaborativeGraph import MultiAgentCollaborativeGraph 
from src.agents.llm_factory import get_llm

def run_collaborative_agents(input_file_path, planner_model, generator_model, verbose): 

    llm_planner = get_llm(provider='groq', model_name=planner_model)
    llm_generator = get_llm(provider='groq', model_name=generator_model)

    agents = MultiAgentCollaborativeGraph(
        input_file_path,
        llm_planner,
        llm_generator,
        verbose
    )

    final_state = agents.invoke()

    ### è da estrarre coverage, iterations etc e ritornarle se si vogliono fare statistiche nell'esperimento
    return {
        "...": 0
    }