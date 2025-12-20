
## HOW TO RUN

### Install Dependencies

```bash
pip install -r requirements.txt
```

### API_KEY

Go to https://console.groq.com/keys and generate an API_KEY, then put in on the .env file
```bash
GROQ_API_KEY = my_key
```

### HOW TO RUN

Run the experimets .py files from the project root (cwd should be that).

You can also run the generated tests by yourself with:

```bash
python -m pytest data/output_tests/baseline/test_bank_account.py 
```

## PROJECT STRUCTURE


![alt text](image.png)

## Packages Overview
### LLM and Agent Management

Framework for agent orchestration. CrewAI excellent for defining specific "roles" (e.g. Generator vs Reviewer), explicitly required.

**langchain** / **langchain-openai**: For base interaction with LLMs.

**python-dotenv**: To securely manage API keys.

### Testing and Evaluation (Minimum Requirements)

**pytest**: The standard framework for running generated tests.

**pytest-cov**: Plugin to calculate line/branch coverage.

**mutmut** or **cosmic-ray**: For mutation testing (verify if tests "kill" mutants, i.e., if they find artificially introduced bugs).

### Data Analysis
**pandas**: To organize metric results.

**matplotlib** / **seaborn**: To create graphs for the report

--------------

## 1. The Scientific Objective
Answer these research questions:

- Do collaborative AI agents generate more complete and varied tests compared to a single LLM? 

- Which collaboration "patterns" work best (e.g. helpful friends vs. harsh critics)? 

## 2. The Software
Implement two distinct systems to compare them:

### A. The Baseline (Single-Agent) (It's a simple script):

- Takes a function as input (e.g. validate_email).

- Asks an LLM : "Write unit tests for this function".

- Saves the result as is.
```bash
python -m pytest data/output_tests/baseline/test_bank_account.py 
```

### B. The Multi-Agent System. A system with at least 2 distinct roles that interact. Test different "patterns":


- **Collaborative**: Agent A writes the test, Agent B suggests improvements ("Could you add a test for empty strings?"), Agent A corrects.

- **Competitive** (Optional but recommended): Agent A writes the test, Agent B actively seeks to find errors in the test or uncovered cases, challenging Agent A.

## 3. The Data (Code Under Test)
- Select 10-20 functions from public datasets or open-source snippets.

- You don't have to write the code to test (you download/find that).

- The system must generate tests for that code.

## 4. The Evaluation (How you score points)
- It's not enough to generate code; you must demonstrate that it works. The document requires at least one of these methods:

    - **Test Coverage**: Run the generated tests and measure how much of the original code they touched (Line Coverage or Branch Coverage).

    - **Mutation Testing**: Use a tool (like **mutmut**) that inserts fake bugs in the original code. If the agents' tests fail, it means they're good (they "caught" the bug). If they still pass, the tests are weak.

## In summary:
- Input: Take a Python function (e.g. calculate_discount).

- Baseline Execution: The single LLM generates test_discount_v1.py.

- Multi-Agent Execution:

    - Tester Agent generates a draft.

    - Reviewer Agent says: "Missing the negative discount case".

    - Tester Agent generates test_discount_final.py.

    Comparison:

    - Run pytest --cov on both files.

    - If the Multi-Agent has 100% coverage and the Baseline 80%, you've won (and proven the thesis).
