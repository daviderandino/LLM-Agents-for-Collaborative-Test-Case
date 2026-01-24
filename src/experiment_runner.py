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
from src.utils.mutmut_runner import get_mutation_metrics
from src.utils.code_parser import remove_failed_tests, syntax_check
from src.utils.pytest_runner import run_pytest


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
    
    for input_file_path in files:
        filename = input_file_path.name
        logger.info(f"--- Processing: {filename} ---")
        
        metrics = None
        
        try:
            # Pass temperature to the runners
            if strategy == "single_agent":
                metrics = run_single_agent(
                    input_file_path=str(input_file_path),
                    output_dir=output_dir,
                    model=cfg.get('llm', 'model'),
                    temperature=temperature 
                )

            elif strategy == "collaborative_agents":
                metrics = run_collaborative_agents(
                    input_file_path=str(input_file_path),
                    output_dir=output_dir,
                    planner_model=cfg.get('llm', 'planner_model'),
                    generator_model=cfg.get('llm', 'generator_model'),
                    planner_temperature=cfg.get('llm', 'planner_temperature') or temperature,
                    generator_temperature=cfg.get('llm', 'generator_temperature') or temperature,
                    verbose=cfg.get('agent', 'verbose'),
                    max_iterations=cfg.get('agent', 'max_iterations') or 10
                )

            elif strategy == "competitive_agents":
                metrics = run_competitive_agents(
                    input_file_path=str(input_file_path),
                    output_dir=output_dir,
                    planner_model=cfg.get('llm', 'planner_model'),
                    generator_model_1=cfg.get('llm', 'generator_model_1'),
                    generator_model_2=cfg.get('llm', 'generator_model_2'),
                    planner_temperature=cfg.get('llm', 'planner_temperature') or temperature,
                    generator_1_temperature=cfg.get('llm', 'generator_1_temperature') or temperature,
                    generator_2_temperature=cfg.get('llm', 'generator_2_temperature') or temperature,
                    verbose=cfg.get('agent', 'verbose'),
                    max_iterations=cfg.get('agent', 'max_iterations') or 10
                )
            
            else:
                logger.error(f"Unknown strategy: {strategy}")
                break

            # --- Prepare test file path ---
            test_filename = f"test_{input_file_path.stem}.py"
            test_file_path = Path("data") / "output_tests" / output_dir / test_filename

            # --- SYNTAX CHECK: Verify the generated test file has valid Python syntax ---
            if test_file_path.exists():
                with open(str(test_file_path), "r") as f:
                    test_code = f.read()
                
                is_valid, syntax_error = syntax_check(test_code)
                if not is_valid:
                    logger.error(f"❌ Syntax error in generated test file: {syntax_error}")
                    results_summary.append(
                        {
                            "file": filename, 
                            "status": "failed", 
                            "error": f"Syntax error in generated test: {syntax_error}",
                            "metrics": metrics
                        }
                    )
                    continue  # Skip this file and move to the next one
            else:
                logger.error(f"❌ Test file not found: {test_file_path}")
                results_summary.append(
                    {
                        "file": filename, 
                        "status": "failed", 
                        "error": f"Test file not generated: {test_file_path}",
                        "metrics": metrics
                    }
                )
                continue

            # --- CLEANUP STEP: Remove failed tests if any ---
            if metrics and metrics["n_failed_tests"] > 0:
                logger.info(f"🧹 Cleanup: Removing {metrics['n_failed_tests']} failed tests...")
                
                if test_file_path.exists():
                    with open(str(test_file_path), "r") as f:
                        test_code = f.read()
                    
                    # Remove failed tests
                    cleaned_code = remove_failed_tests(test_code, metrics["failed_tests_infos"])
                    
                    # Recalculate metrics after cleanup
                    from src.utils.file_manager import obtain_import_module_str
                    target_module = obtain_import_module_str(str(input_file_path))
                    report = run_pytest(target_module, cleaned_code)
                    
                    # Update metrics
                    metrics["coverage_percent"] = report["coverage"]
                    
                    # Write the cleaned code back
                    with open(str(test_file_path), "w") as f:
                        f.write(cleaned_code)
                    
                    logger.info(f"✓ Cleanup complete. New metrics - Coverage: {metrics['coverage_percent']}%, Passed: {metrics['n_passed_tests']}, Failed: {metrics['n_failed_tests']}")

            # --- MUTATION TESTING STEP ---
            if metrics: #Note: we are assuming that the prefious if correctly removed failed tests
                logger.info(f"🧬 Running mutation testing...")
                mutation_result = get_mutation_metrics(
                    source_file_path=str(input_file_path),
                    test_file_path=str(test_file_path),
                )

                if mutation_result is not None:
                    metrics["mutation_score_percent"] = mutation_result["mutation_score_percent"]
                    metrics["mutation_killed"] = mutation_result["mutation_killed"]
                    metrics["mutation_survived"] = mutation_result["mutation_survived"]
                else:
                    metrics["mutation_score_percent"] = None
                    metrics["mutation_killed"] = None
                    metrics["mutation_survived"] = None
            else:
                logger.warning(f"⚠️ Skipping mutation testing for {filename}: test execution produced failures")
            
            results_summary.append(
                    {
                        "file": filename, 
                        "status": "success", 
                        "metrics": metrics
                    }
                )

            logger.info(f"Metrics for {filename}: {metrics}")

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
        if hasattr(cfg, 'run_id') and isinstance(cfg.run_id, str):
            cfg.run_id = cfg.run_id.replace(":", "-")
    except Exception as e:
        print(f"❌ Could not load config: {e}")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
    
    # cfg.save_snapshot() disabled snapshot
    results = run_experiment(cfg)

    # Save Metrics (Placeholders Filled!)
    if results and len(results) > 0:
        save_run_metrics(config_manager=cfg, results=results)
    else:
        print("⚠️ No valid results to save.")

if __name__ == "__main__":

    run()
