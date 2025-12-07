"""
Intended for the simple, single-agent system
"""

from src.llm_factory import get_llm
from langchain.prompts import PromptTemplate

# I can change 'groq' to 'colab' without touching the rest of the code!
llm = get_llm(provider="groq", model_name="llama3-8b-8192", temperature=0)