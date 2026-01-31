
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

#### Option 1: Run Experiments via Command Line

```bash
python src/experiment_runner.py --config configs/experiments/{experiment_name}.yaml
```

Example:
```bash
python src/experiment_runner.py --config configs/experiments/single_gptoss120B.yaml
```

#### Option 2: Run via Jupyter Notebook

Open and run `experiments.ipynb` to execute experiments interactively.

#### Option 3: Analyze Results

After running experiments:

1. **Export metrics to CSV**:
   ```bash
   python export_metrics_as_csv.py
   ```
   This creates `all_metrics.csv` with aggregated results.

2. **Run mutation testing** (optional):
   Open and run `mutation_injection.ipynb` to inject mutations and measure test quality.

3. **View metrics visualization**:
   Open and run `metrics_aggregation.ipynb` to see aggregated metrics by experiment with charts.

## Packages Overview

### LLM and Agent Management
- **langchain** / **langchain-core**: For base interaction with LLMs and prompt templates
- **langgraph**: Framework for agent orchestration with state graphs (replaces manual agent coordination)
- **python-dotenv**: To securely manage API keys

### Testing and Evaluation
- **pytest**: The standard framework for running generated tests
- **pytest-cov**: Plugin to calculate line/branch code coverage
- **mutmut**: For mutation testing (verify if tests "kill" mutants - artificially injected bugs)

### Data Analysis & Visualization
- **pandas**: To organize and aggregate metric results
- **matplotlib**: To create comparison charts and visualizations
- **numpy**: For numerical computations and statistics

### Configuration
- **PyYAML**: For loading experiment configuration files

## Output & Metrics

### Results Directory Structure
Each experiment creates a JSON file in `results/` with:
- `run_id`: Unique identifier (experiment_name + timestamp)
- `experiment_name`: Name of the configuration used
- `timestamp`: When the experiment was run
- `temperature`: LLM temperature parameter
- `results[]`: Array containing per-file results:
  - `file`: Source file name
  - `status`: success/failure
  - `metrics`:
    - `coverage_percent`: Line coverage percentage
    - `mutation_score_percent`: Mutation test success rate
    - `mutation_killed`: Number of mutations killed by tests
    - `mutation_survived`: Number of undetected mutations
    - `total_tokens`: LLM tokens used

### Analysis Notebooks
- **metrics_aggregation.ipynb**: Aggregates metrics by experiment_name, shows mean/std for coverage, mutation score, and tokens
- **mutation_injection.ipynb**: Runs mutation testing where missing, adds mutation metrics to results

### CSV Export
`export_metrics_as_csv.py` generates `all_metrics.csv` for easy analysis in Excel/Pandas

## Agent Architectures

### Single Agent
- One LLM generates all tests from scratch
- Baseline for comparison

### Multi-Agent Collaborative
- **Planner**: Creates test plan JSON
- **Developer**: Generates test code from plan
- **Executor**: Runs tests and measures coverage
- **Feedback Loop**: Re-plans to fill coverage gaps

### Multi-Agent Competitive
- **Planner**: Creates test plan
- **Developer 1 & 2**: Simultaneously generate different test implementations
- **Executor**: Runs both and selects best based on coverage/quality
- Strategy focuses on diverse test generation approaches

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

- **Competitive**: Agent A writes the test, Agent B actively seeks to find errors in the test or uncovered cases, challenging Agent A.

## 3. The Data (Code Under Test)
- Select 10-20 functions from public datasets or open-source snippets.

- You don't have to write the code to test (you download/find that).

- The system must generate tests for that code.

## 4. The Evaluation (How you score points)
- It's not enough to generate code; you must demonstrate that it works. The document requires at least one of these methods:

    - **Test Coverage**: Run the generated tests and measure how much of the original code they touched (Line Coverage or Branch Coverage).

    - **Mutation Testing**: Use a tool (**mutmut**) that inserts fake bugs in the original code. If the agents' tests fail, it means they're good (they "caught" the bug). If they still pass, the tests are weak.
    - 
- TO RUN: python run.py --config configs/experiments/{experiment_name}.yaml
