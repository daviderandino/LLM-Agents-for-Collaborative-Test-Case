from src.agents.single_agent.SingleAgentChain import SingleAgentChain
from src.agents.llm_factory import get_llm

def run_single_agent(input_file_path, model): 

    llm = get_llm(provider='groq', model_name=model)

    agent = SingleAgentChain(input_file_path, llm)

    final_state = agent.invoke()

    ### è da estrarre coverage, iterations etc e ritornarle se si vogliono fare statistiche nell'esperimento
    return {
        "...": 0
    }