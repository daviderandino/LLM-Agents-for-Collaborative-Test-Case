![alt text](image.png)

### A. Gestione LLM e Agenti

Framework per l'orchestrazione degli agenti. CrewAI ottimo per definire "ruoli" specifici (es. Generator vs Reviewer), richiesti esplicitamente.

langchain / langchain-openai: Per l'interazione base con gli LLM.

python-dotenv: Per gestire le chiavi API in sicurezza.

### B. Testing e Valutazione (Requisiti Minimi)

pytest: Il framework standard per eseguire i test generati.

pytest-cov: Plugin per calcolare la line/branch coverage.

mutmut o cosmic-ray: Per il mutation testing (verificare se i test "uccidono" i mutanti, ovvero se trovano bug introdotti artificialmente).

### C. Analisi Dati
pandas: Per organizzare i risultati delle metriche.

matplotlib / seaborn: Per creare i grafici da inserire nel report

--------------

## 1. L'Obiettivo Scientifico
Rispondere a queste domande di ricerca:

- Gli agenti AI collaborativi generano test più completi e vari rispetto a un singolo LLM? 

- Quali "pattern" di collaborazione funzionano meglio (es. amici che si aiutano vs. critici severi)? 

## 2. Il Software
Implementare due sistemi distinti per confrontarli:

### A. La Baseline (Single-Agent) (È uno script semplice):

- Prende in input una funzione (es. validate_email).

- Chiede a un LLM (es. GPT-4o-mini): "Scrivi i test unitari per questa funzione".

- Salva il risultato così com'è.

### B. Il Sistema Multi-Agent. Un sistema con almeno 2 ruoli distinti che interagiscono. Testare diversi "pattern":


- Collaborativo: Agente A scrive il test, Agente B suggerisce miglioramenti ("Potresti aggiungere un test per le stringhe vuote?"), Agente A corregge.

- Competitivo (Opzionale ma consigliato): Agente A scrive il test, Agente B cerca attivamente di trovare errori nel test o casi non coperti, sfidando l'Agente A.

## 3. I Dati (Code Under Test)
- Selezionare 10-20 funzioni da dataset pubblici o snippet open-source.

- Non devi scrivere il codice da testare (quello lo scarichi/trovi).

- Il sistema deve generare i test per quel codice.

## 4. La Valutazione (Come prendi i punti)
- Non basta generare codice; bisogna dimostrare che funziona. Il documento richiede almeno uno di questi metodi:

    - Test Coverage: Eseguire i test generati e misurare quanta parte del codice originale hanno toccato (Line Coverage o Branch Coverage).

    - Mutation Testing: Usanre un tool (come mutmut) che inserisce bug finti nel codice originale. Se i test degli agenti falliscono, significa che sono buoni (hanno "catturato" il bug). Se passano comunque, i test sono deboli.

## In sintesi:
- Input: Prendi una funzione Python (es. calcola_sconto).

- Esecuzione Baseline: L'LLM singolo genera test_sconto_v1.py.

- Esecuzione Multi-Agent:

    - Tester Agent genera una bozza.

    - Reviewer Agent dice: "Manca il caso dello sconto negativo".

    - Tester Agent genera test_sconto_final.py.

    Confronto:

    - Lanci pytest --cov su entrambi i file.

    - Se il Multi-Agent ha il 100% di coverage e la Baseline l'80%, hai vinto (e dimostrato la tesi).