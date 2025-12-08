"""
Centralizza e semplifica la creazione delle istanze dei modelli LLM.
Segue un Factory Pattern.
"""

import os
from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFacePipeline # O Ollama, o LlamaCPP


def get_llm(provider="groq", model_name="llama3-70b-8192", temperature=0):
    """
    Factory function per cambiare modello facilmente.
    Questo dimostra che il sistema non è vincolato ad usare solo Groq.

    Note: 'llama3-70b-8192' è molto potente, ha una context window di >8000 token.
    """

    if provider == "groq":
        return ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=os.getenv("GROQ_API_KEY")
        )
    elif provider == "local_colab":
        pass