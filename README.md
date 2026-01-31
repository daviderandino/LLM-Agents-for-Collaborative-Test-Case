
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
   
- TO RUN: python run.py --config configs/experiments/{experiment_name}.yaml
