import os
from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFacePipeline # O Ollama, o LlamaCPP

def get_llm(model_type="groq"):
    """
    Factory function per cambiare modello facilmente.
    Questo dimostra che il tuo sistema non è 'bloccato' su Groq.
    """
    if model_type == "groq":
        return ChatGroq(
            temperature=0,
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
    elif model_type == "local_colab":
        pass