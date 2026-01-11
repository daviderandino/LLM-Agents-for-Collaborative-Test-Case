import os
import json
import numpy as np
import matplotlib.pyplot as plt


def plot_metrics(results_dir='results'):
    """
    Legge tutte le cartelle dentro 'results', parsa metrics.json 
    e genera un grafico comparativo.
    """
    
    experiment_data = []

    if not os.path.exists(results_dir):
        print(f"Errore: La cartella '{results_dir}' non esiste.")
        return

    # Ordino le cartelle
    subdirs = sorted([d for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d))])

    for experiment_name in subdirs:
        metric_path = os.path.join(results_dir, experiment_name, 'metrics.json')
        
        if not os.path.exists(metric_path):
            continue

        try:
            with open(metric_path, 'r') as f:
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
            
            if not mutations:
                avg_mutation = 0
            else:
                avg_mutation = np.mean(mutations)
                
            avg_tokens = np.mean(tokens) if tokens else 0

            experiment_data.append({
                'name': experiment_name,
                'coverage': avg_coverage,
                'mutation': avg_mutation,
                'tokens': avg_tokens
            })

        except Exception as e:
            print(f"Errore leggendo {experiment_name}: {e}")

    if not experiment_data:
        print("Nessun dato valido trovato.")
        return

    names = [item['name'] for item in experiment_data]
    cov_vals = [item['coverage'] for item in experiment_data]
    mut_vals = [item['mutation'] for item in experiment_data]
    tok_vals = [item['tokens'] for item in experiment_data]

    x = np.arange(len(names))  # posizioni delle etichette
    width = 0.25  # larghezza delle barre

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # creazione asse secondario per i Token (hanno scala diversa)
    ax2 = ax1.twinx()

    # barre Coverage (Verde) e Mutation (Blu) su asse Sinistro (Percentuale)
    rects1 = ax1.bar(x - width, cov_vals, width, label='Coverage', color='#74c476')
    rects2 = ax1.bar(x, mut_vals, width, label='Mutation Score', color='#4dabf5')
    
    # barra Tokens (Arancione) su asse Destro (Valore assoluto)
    rects3 = ax2.bar(x + width, tok_vals, width, label='Avg Tokens', color='#ff9800', alpha=0.7)

    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=30, ha='right')
    ax1.set_ylim(0, 115) 
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # Legenda combinata
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

    # aggiunge etichette sopra le barre
    def autolabel(rects, ax, format_str='{:.1f}%'):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                format_str.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

    autolabel(rects1, ax1, '{:.1f}%')
    autolabel(rects2, ax1, '{:.1f}%')
    autolabel(rects3, ax2, '{:.0f}')

    plt.tight_layout()
    plt.show()