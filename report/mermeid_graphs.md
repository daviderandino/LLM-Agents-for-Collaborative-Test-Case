# Mermaid Diagrams - Collaborative JSON Graph

---

## 1. PLANNER Node

```mermaid
%%{init: { 
  'flowchart': { 'nodeSpacing': 5, 'rankSpacing': 30,  'padding': 10 },
  'themeVariables': { 'fontSize': '10px'} 
}}%%
flowchart LR
    subgraph PLANNER_NODE ["PLANNER NODE"]
        direction LR
        CheckIter{"Is first call?"}
        
        CheckIter -- "Yes" --> Scenario1["Prompt: plan from scratch<br>Input: source code only"]
        CheckIter -- "No" --> Scenario2["Prompt: increase coverage<br>Input: code + tests + coverage%"]
        
        Scenario1 --> InvokeLLM1["Invoke Planner LLM"]
        Scenario2 --> InvokeLLM2["Invoke Planner LLM"]
        
        InvokeLLM1 --> Return1(["Save full plan to state"])
        InvokeLLM2 --> SaveIncremental(["Merge with previous state and save"])
    end

    %% Stile del rettangolo (subgraph)
    style PLANNER_NODE fill:#e1f5fe,stroke-width:0px
    
    %% Stili dei nodi interni
    style CheckIter fill:#fff4cc,stroke:#333
    style Scenario1 fill:#cce5ff
    style Scenario2 fill:#cce5ff
    style InvokeLLM1 fill:#e1f5e1
    style InvokeLLM2 fill:#e1f5e1
    style Return1 fill:#ffe1e1,stroke:#333
    style SaveIncremental fill:#ffe1e1,stroke:#333
```

---

## 2. DEVELOPER Node

```mermaid
%%{init: { 
  'flowchart': { 'nodeSpacing': 10, 'rankSpacing': 20, 'padding': 8 },
  'themeVariables': { 'fontSize': '10px'} 
}}%%

flowchart LR
    subgraph DEV_NODE ["DEVELOPER NODE"]
        direction LR
        Select{Start: Select Mode}
        
        Select -- "iter==0" --> M1["Prompt: generate"]
        Select -- "fail>0" --> M2["Prompt: fix"]
        Select -- "error" --> M3["Prompt: syntax"]
        Select -- "else" --> M4["Prompt: append"]
        
        M1 & M2 & M3 --> LLM_R[Invoke LLM]
        M4 --> LLM_A[Invoke LLM]
        
        LLM_R --> Replace(["End: Replace Code"])
        LLM_A --> Append(["End: Append Code"])
    end

    %% Stile del contenitore: verde chiaro, senza bordo
    style DEV_NODE fill:#e8f5e9,stroke-width:0px

    %% Stili dei nodi interni
    style Select fill:#fff4cc,stroke:#333
    style M1 fill:#cce5ff
    style M2 fill:#cce5ff
    style M3 fill:#cce5ff
    style M4 fill:#cce5ff
    style LLM_R fill:#e1f5e1
    style LLM_A fill:#e1f5e1
    style Replace fill:#ffe1e1,stroke:#333
    style Append fill:#ffe1e1,stroke:#333
```

---

## 3. EXECUTOR Node

```mermaid
%%{init: { 
  'flowchart': { 'nodeSpacing': 5, 'rankSpacing': 20, 'padding': 10 },
  'themeVariables': { 'fontSize': '10px'} 
}}%%

flowchart LR
    subgraph VAL_NODE ["EXECUTOR NODE"]
        direction LR
        Check{Syntax Check}
        
        Check -- "Err" --> ErrS(["End: Syntax Error"])
        
        Check -- "OK" --> Pytest[Run Pytest]
        
        Pytest --> Crash{Crash?}
        
        Crash -- "Yes" --> ErrC(["End: Pytest Error"])
        
        Crash -- "No" --> Metrics[Extract Metrics]
        
        Metrics --> Save(["End: Save & Incr"])
    end

    %% Stile del contenitore: giallo chiaro, senza bordo
    style VAL_NODE fill:#fffde7,stroke-width:0px

    %% Stili dei nodi interni
    style Check fill:#fff4cc,stroke:#333
    style Pytest fill:#cce5ff
    style Metrics fill:#ccffcc
    style ErrS fill:#ffe1e1,stroke:#333
    style ErrC fill:#ffe1e1,stroke:#333
    style Save fill:#ffe1e1,stroke:#333
```

---

## 3.1 All in one 

```mermaid
---
config:
  flowchart:
    nodeSpacing: 5
    rankSpacing: 20
    padding: 10
  themeVariables:
    fontSize: 10px
  layout: elk
---
flowchart RL
 subgraph PLANNER_NODE["PLANNER NODE"]
    direction LR
        P_Check{"Is first call?"}
        P_S1["Prompt: plan scratch"]
        P_S2["Prompt: coverage"]
        P_LLM1["Invoke LLM"]
        P_LLM2["Invoke LLM"]
        P_R1(["End: Save Plan"])
        P_R2(["End: Merge State"])
  end
 subgraph DEV_NODE["DEVELOPER NODE"]
    direction LR
        D_Select{"Select Mode"}
        D_M1["Prompt: gen"]
        D_M2["Prompt: fix"]
        D_M3["Prompt: syntax"]
        D_M4["Prompt: app"]
        D_LLM_R["Invoke LLM"]
        D_LLM_A["Invoke LLM"]
        D_Repl(["End: Replace"])
        D_App(["End: Append"])
  end
 subgraph VAL_NODE["EXECUTOR NODE"]
    direction LR
        V_Check{"Syntax Check"}
        V_ErrS(["End: Syntax Error"])
        V_Pytest["Run Pytest"]
        V_Crash{"Crash?"}
        V_ErrC(["End: Pytest Error"])
        V_Metrics["Extract Metrics"]
        V_Save(["End: Save & Incr"])
  end
    P_Check -- Yes --> P_S1
    P_Check -- No --> P_S2
    P_S1 --> P_LLM1
    P_S2 --> P_LLM2
    P_LLM1 --> P_R1
    P_LLM2 --> P_R2
    D_Select -- "iter=0" --> D_M1
    D_Select -- fail>0 --> D_M2
    D_Select -- err --> D_M3
    D_Select -- else --> D_M4
    D_M1 --> D_LLM_R
    D_M2 --> D_LLM_R
    D_M3 --> D_LLM_R
    D_M4 --> D_LLM_A
    D_LLM_R --> D_Repl
    D_LLM_A --> D_App
    V_Check -- Err --> V_ErrS
    V_Check -- OK --> V_Pytest
    V_Pytest --> V_Crash
    V_Crash -- Yes --> V_ErrC
    V_Crash -- No --> V_Metrics
    V_Metrics --> V_Save

    style P_Check fill:#fff4cc,stroke:#333
    style P_S1 fill:#cce5ff
    style P_S2 fill:#cce5ff
    style P_R1 fill:#ffe1e1,stroke:#333
    style P_R2 fill:#ffe1e1,stroke:#333
    style D_Select fill:#fff4cc,stroke:#333
    style D_M1 fill:#cce5ff
    style D_M2 fill:#cce5ff
    style D_M3 fill:#cce5ff
    style D_M4 fill:#cce5ff
    style D_Repl fill:#ffe1e1,stroke:#333
    style D_App fill:#ffe1e1,stroke:#333
    style V_Check fill:#fff4cc,stroke:#333
    style V_ErrS fill:#ffe1e1,stroke:#333
    style V_Pytest fill:#cce5ff
    style V_ErrC fill:#ffe1e1,stroke:#333
    style V_Save fill:#ffe1e1,stroke:#333
    style PLANNER_NODE fill:#e1f5fe,stroke-width:0px
    style DEV_NODE fill:#e8f5e9,stroke-width:0px
    style VAL_NODE fill:#fffde7,stroke-width:0px
```

---

## 4. Collaborative Workflow

```mermaid
---
config:
  flowchart:
    nodeSpacing: 25
    rankSpacing: 30
  themeVariables:
    fontSize: 10px
  layout: dagre
---
flowchart TB
    Start["code.py"] --> Planner["PLANNER"]
    Planner --> Developer["DEVELOPER"]
    Developer --> Executor["EXECUTOR"]
    Executor -- "1. Check: iterations >= max?" --> EndTimeout(["END<br>Timeout"])
    Executor -- "2. Check: has errors or fails?" --> Developer
    Executor -- "3. Check: coverage &lt; 100%?" --> Planner
    Executor -- "4. Else: success<br>(coverage = 100% AND no errors)" --> EndSuccess(["END<br>Success"])

    Start@{ shape: doc}
    style Planner fill:#cce5ff
    style Developer fill:#ccffcc
    style Executor fill:#fff4cc
    style EndTimeout fill:#ffe1e1
    style EndSuccess fill:#ffe1e1
```

---

## 5. Competitive Workflow

```mermaid
---
config:
  flowchart:
    nodeSpacing: 25
    rankSpacing: 30
  themeVariables:
    fontSize: 10px
  layout: dagre
---
flowchart TB
    Start["code.py"] --> Planner["PLANNER"]
    Planner --> Developer["Dev1 AND Dev2"]

    Developer --> Executor["EXECUTOR:</br> Compare & Select Winner"]
    Executor -- "1. Check: iterations >= max?" --> EndTimeout(["END<br>Timeout"])
    Executor -- "2. Check: has errors or fails?" --> Developer
    Executor -- "3. Check: coverage &lt; 100%?" --> Planner
    Executor -- "4. Else: success<br>(coverage = 100% AND no errors)" --> EndSuccess(["END<br>Success"])

    Start@{ shape: doc}
    style Planner fill:#cce5ff
    style Developer fill:#ccffcc
    style Executor fill:#fff4cc
    style EndTimeout fill:#ffe1e1
    style EndSuccess fill:#ffe1e1
```

