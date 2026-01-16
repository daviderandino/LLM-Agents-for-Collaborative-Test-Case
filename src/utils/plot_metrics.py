import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_metrics(results_dir='results'):
    """
    Reads all JSON files in results directory and generates comparative graphs.
    """
    experiment_data = []
    
    results_path = Path(results_dir)
    if not results_path.exists():
        print(f"Error: '{results_dir}' directory does not exist.")
        return
    
    # Read all JSON files in results folder
    json_files = sorted(results_path.glob('*.json'))
    
    for json_file in json_files:
        experiment_name = json_file.stem
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            file_results = data.get('results', [])
            
            if not file_results:
                continue
            
            coverages = []
            mutations = []
            tokens = []
            
            for res in file_results:
                metrics = res.get('metrics', {})
                coverages.append(metrics.get('coverage_percent', 0))
                mut_score = metrics.get('mutation_score_percent')
                if mut_score is not None:
                    mutations.append(mut_score)
                tokens.append(metrics.get('total_tokens', 0))
            
            avg_coverage = np.mean(coverages) if coverages else 0
            avg_mutation = np.mean(mutations) if mutations else 0
            avg_tokens = np.mean(tokens) if tokens else 0
            
            experiment_data.append({
                'name': experiment_name,
                'coverage': avg_coverage,
                'mutation': avg_mutation,
                'tokens': avg_tokens
            })
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    if not experiment_data:
        print("No experiment data found.")
        return
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    names = [d['name'] for d in experiment_data]
    coverages = [d['coverage'] for d in experiment_data]
    mutations = [d['mutation'] for d in experiment_data]
    tokens = [d['tokens'] for d in experiment_data]
    
    # Plot coverage
    axes[0].bar(range(len(names)), coverages, color='skyblue', alpha=0.8)
    axes[0].set_xticks(range(len(names)))
    axes[0].set_xticklabels(names, rotation=45, ha='right')
    axes[0].set_ylabel('Coverage (%)')
    axes[0].set_title('Average Coverage by Experiment')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Plot mutation score
    axes[1].bar(range(len(names)), mutations, color='lightcoral', alpha=0.8)
    axes[1].set_xticks(range(len(names)))
    axes[1].set_xticklabels(names, rotation=45, ha='right')
    axes[1].set_ylabel('Mutation Score (%)')
    axes[1].set_title('Average Mutation Score by Experiment')
    axes[1].grid(axis='y', alpha=0.3)
    
    # Plot tokens
    axes[2].bar(range(len(names)), tokens, color='lightgreen', alpha=0.8)
    axes[2].set_xticks(range(len(names)))
    axes[2].set_xticklabels(names, rotation=45, ha='right')
    axes[2].set_ylabel('Total Tokens')
    axes[2].set_title('Average Tokens Used by Experiment')
    axes[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
