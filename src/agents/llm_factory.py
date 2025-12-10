"""
Centralizza e semplifica la creazione delle istanze dei modelli LLM.
Segue un Factory Pattern.
"""

import os
from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFacePipeline # O Ollama, o LlamaCPP

# MEGLIO LA VERSIONE INSTRUCT DEI MODELLI ???
def get_llm(provider="groq", model_name="llama-3.3-70b-versatile", temperature=0):
    """
    Factory function per cambiare modello facilmente.
    Questo dimostra che il sistema non è vincolato ad usare solo Groq.
    """

    if provider == "groq":
        return ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=os.getenv("GROQ_API_KEY")
        )
    elif provider == "local_colab":
        pass