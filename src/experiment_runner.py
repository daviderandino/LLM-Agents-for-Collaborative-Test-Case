# src/main.py
import argparse
import sys
import os
import logging
from pathlib import Path
from tqdm import tqdm

# Config System
from src.ConfigManager import ConfigManager
from src.tracker import save_run_metrics

# Agent Runners (Corrected Imports)
from src.agents.single_agent.single_agent_runner import run_single_agent
from src.agents.multi_agent_collaborative.multi_agent_collaborative_runner import run_collaborative_agents
from src.agents.multi_agent_competitive.multi_agent_competitive_runner import run_competitive_agents


def get_files_to_process(input_path_str):
    path = Path(input_path_str)
    if not path.exists():
        raise FileNotFoundError(f"Input path not found: {input_path_str}")
    
    if path.is_file():
        return [path]
    elif path.is_dir():
        return [f for f in path.glob("*.py") if f.name != "__init__.py"]
    else:
        return []

def run_experiment(cfg):
    logger = logging.getLogger("Orchestrator")
    
    # 1. Determine Strategy and Settings
    strategy = cfg.get('experiment', 'type')
    input_path = cfg.get('experiment', 'input_path')
    output_dir = cfg.run_id  # Use the unique run_id from ConfigManager
    temperature = cfg.get('llm', 'temperature') 
    
    logger.info(f"🚀 Starting Experiment. Strategy: {strategy}")
    logger.info(f"📂 Input Path: {input_path}")
    logger.info(f"🌡️  Temperature: {temperature}")

    files = get_files_to_process(input_path)
    logger.info(f"📝 Found {len(files)} file(s) to process.")

    results_summary = []
    
    for file_path in files:
        filename = file_path.name
        logger.info(f"--- Processing: {filename} ---")
        
        file_result = None
        
        try:
            # Pass temperature to the runners
            if strategy == "single_agent":
                file_result = run_single_agent(
                    input_file_path=str(file_path),
                    output_dir=output_dir,
                    model=cfg.get('llm', 'model'),
                    temperature=temperature 
                )

            elif strategy == "collaborative_agents":
                file_result = run_collaborative_agents(
                    input_file_path=str(file_path),
                    output_dir=output_dir,
                    planner_model=cfg.get('llm', 'planner_model'),
                    generator_model=cfg.get('llm', 'generator_model'),
                    temperature=temperature, 
                    verbose=cfg.get('agent', 'verbose')
                )

            elif strategy == "competitive_agents":
                file_result = run_competitive_agents(
                    input_file_path=str(file_path),
                    output_dir=output_dir,
                    planner_model=cfg.get('llm', 'planner_model'),
                    generator_model_1=cfg.get('llm', 'generator_model_1'),
                    generator_model_2=cfg.get('llm', 'generator_model_2'),
                    temperature=temperature,
                    verbose=cfg.get('agent', 'verbose')
                )
            
            else:
                logger.error(f"Unknown strategy: {strategy}")
                continue

            if file_result:
                results_summary.append(
                    {
                        "file": filename, 
                        "status": "success", 
                        "metrics": file_result
                    }
                )

        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}", exc_info=True)
            results_summary.append({"file": filename, "status": "error", "error": str(e)})

    logger.info("--- 🏁 Experiment Complete ---")

    return results_summary

def run():
    parser = argparse.ArgumentParser(description="AI Agent Experiment Runner")
    parser.add_argument("--config", type=str, default=None, help="Path to experiment config")
    args = parser.parse_args()

    try:
        cfg = ConfigManager(args.config)
    except Exception as e:
        print(f"❌ Could not load config: {e}")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # cfg.save_snapshot() disabled snapshot
    results = run_experiment(cfg)

    # Save Metrics (Placeholders Filled!)
    if results and len(results) > 0:
        save_run_metrics(config_manager=cfg, results=results)
    else:
        print("⚠️ No valid results to save.")

if __name__ == "__main__":
    run()