## COME FUNZIONA FINORA

Runnare gli esperimenti dalla root del progetto, gli agenti genereranno i test nelle rispetive cartelle in data/output_tests a partire da un file dentro data/input_code.

Si può poi eseguire manualmente i test con:

```bash
python -m pytest data/output_tests/ARCHITETTURA_AGENTICA/test_XYZ.py 
```

## AGGIUNGERE DATASET E FARE LOOP SUL DATASET

baseline_agent.py va integrato col dataset, come richiesto dai requisiti del progetto

Attualmente baseline_agent.py funziona su un file alla volta, non è scalabile.

Usare uno script "orchestratore" (src/main.py ) per eseguire l'agente su tutti i file del dataset in sequenza.

1. Prepara la cartella dei dati

Il "dataset" non è altro che una collezione di file Python.

Nella cartella data/input_code/ inserire lì 10-20 file .py presi da MBPP, HumanEval o GitHub.

Importante: Creare un file vuoto chiamato __init__.py dentro data/input_code/. Questo serve a Python per trattare la cartella come un "pacchetto", permettendo ai test generati di fare from input_code.nome_file import ....

2. Usare main.py per il loop

Il file src/main.py servirà proprio a lanciare la generazione su tutto il set.

## POI... MULTIAGENT

## BASELINE VS MULTIAGENT

Bisogna dimostrare che un sistema collaborativo (Multi-Agent) è migliore di un singolo LLM. Per farlo, serve un termine di paragone "semplice": un singolo LLM che prova a scrivere i test da solo, senza aiuti o revision

Lo scopo è stabilire l'asticella: se il baseline_agent ottiene l'80% di coverage, il tuo sistema Multi-Agente dovrà superare quell'80% per essere considerato un successo.