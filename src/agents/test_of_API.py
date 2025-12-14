"""
Prova di funzionamento API di Groq.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Carica le chiavi dal file .env
load_dotenv()

# Configura Groq
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Leggi il codice da testare
with open("data/input_code/bank_account.py", "r") as f:
    code_snippet = f.read()

# Prova
print("Chiedo a Llama 3.1-8b di analizzare il codice...")
response = llm.invoke(f"Spiegami in una frase cosa fa questo codice:\n\n{code_snippet}")

print("\nRISPOSTA GROQ:")
print(response.content)