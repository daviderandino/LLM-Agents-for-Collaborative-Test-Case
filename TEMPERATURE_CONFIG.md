# Individual Temperature Configuration

## Overview
Set different temperatures for each agent in collaborative and competitive setups for fine-grained control over agent behavior.

## Configuration

### Collaborative Agents
```yaml
llm:
  planner_model: "openai/gpt-oss-20b"
  generator_model: "openai/gpt-oss-120b"
  planner_temperature: 0.1    # Default: 0
  generator_temperature: 0.4   # Default: 0
```

### Competitive Agents
```yaml
llm:
  planner_model: "meta-llama/llama-4-scout-17b-16e-instruct"
  generator_model_1: "openai/gpt-oss-120b"
  generator_model_2: "llama-3.3-70b-versatile"
  planner_temperature: 0.0       # Default: 0
  generator_1_temperature: 0.3   # Default: 0
  generator_2_temperature: 0.5   # Default: 0
```

## Examples
- `configs/experiments/collaborative_custom_temps_example.yaml`
- `configs/experiments/competitive_custom_temps_example.yaml`

## Modified Files
- `src/agents/multi_agent_collaborative/multi_agent_collaborative_runner.py`
- `src/agents/multi_agent_competitive/multi_agent_competitive_runner.py`
- `src/experiment_runner.py`
