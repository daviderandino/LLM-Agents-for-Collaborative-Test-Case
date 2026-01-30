import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

INPUT_FOLDER = './results' 
OUTPUT_FOLDER = './graphs_tokens'

# ============================================================================

def classify_experiment(experiment_name):
    """
    Classifica l'esperimento in base al nome (Single, Collaborative, Competitive)
    e alla 'forza' del modello (Strong, Weak, Mix).
    """
    name_lower = experiment_name.lower()
    
    # Determina il mode
    if 'collaborative' in name_lower:
        mode = 'collaborative'
    elif 'competitive' in name_lower:
        mode = 'competitive'
    elif 'single' in name_lower:
        mode = 'single'
    else:
        return None, None
    
    # Modelli strong e weak
    strong_models = ['gptoss120b', 'llama70b']
    weak_models = ['gptoss20b', 'llama17b', 'llamascout17b']
    
    # Conta i modelli presenti nel nome
    strong_count = sum(1 for model in strong_models if model in name_lower)
    weak_count = sum(1 for model in weak_models if model in name_lower)
    
    # Determina strength
    if mode == 'single':
        if strong_count > 0:
            strength = 'strong'
        elif weak_count > 0:
            strength = 'weak'
        else:
            strength = 'unknown'
    else:  # collaborative o competitive
        if strong_count > 0 and weak_count == 0:
            strength = 'strong'
        elif weak_count > 0 and strong_count == 0:
            strength = 'weak'
        elif strong_count > 0 and weak_count > 0:
            strength = 'mix'
        else:
            strength = 'unknown'
    
    return mode, strength

def load_experiments(input_folder):
    """Carica i dati dai file JSON."""
    experiments = defaultdict(lambda: defaultdict(list))
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Attenzione: La cartella {input_folder} non esiste.")
        return experiments

    json_files = list(input_path.glob('*.json'))
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            experiment_name = data.get('experiment_name', '')
            mode, strength = classify_experiment(experiment_name)
            
            if mode and strength:
                experiments[mode][strength].append(data)
        except Exception as e:
            print(f"Errore leggendo {json_file}: {e}")
    return experiments

def aggregate_tokens(experiments):
    """Estrae i token totali per ogni file e configurazione."""
    # Struttura: aggregated[filename][exp_type] = lista di valori token
    aggregated = defaultdict(lambda: defaultdict(list))
    
    experiment_types = [
        ('single', 'strong'),
        ('single', 'weak'),
        ('collaborative', 'strong'),
        ('collaborative', 'mix'),
        ('collaborative', 'weak'),
        ('competitive', 'strong'),
        ('competitive', 'mix'),
        ('competitive', 'weak')
    ]
    
    for mode, strength in experiment_types:
        if mode in experiments and strength in experiments[mode]:
            for exp_data in experiments[mode][strength]:
                for result in exp_data.get('results', []):
                    filename = result['file']
                    metrics = result.get('metrics', {})
                    # Usa 'total_tokens' dal JSON
                    tokens = metrics.get('total_tokens', 0)
                    
                    exp_type = f"{mode}_{strength}"
                    aggregated[filename][exp_type].append(tokens)
    
    # Calcola la media dei token per ogni (file, tipo_esperimento)
    final_data = defaultdict(dict)
    for filename in aggregated:
        for exp_type in aggregated[filename]:
            values = aggregated[filename][exp_type]
            final_data[filename][exp_type] = np.mean(values) if values else 0
            
    return final_data

def plot_token_usage(aggregated_data, output_folder):
    """Genera e salva il grafico dei token."""
    
    # Ordina i file: prima dNN poi gli altri
    dnn_files = sorted([f for f in aggregated_data.keys() if f.startswith('d') and f[1:3].isdigit()])
    other_files = sorted([f for f in aggregated_data.keys() if not (f.startswith('d') and f[1:3].isdigit())])
    files = dnn_files + other_files
    
    # Aggiungi colonna MEAN finale
    files_with_mean = files + ['MEAN']
    
    # Raggruppamenti per il grafico
    experiment_groups = [
        ['single_strong', 'single_weak'],
        ['collaborative_strong', 'collaborative_mix', 'collaborative_weak'],
        ['competitive_strong', 'competitive_mix', 'competitive_weak']
    ]
    
    exp_labels = {
        'single_strong': 'Single Strong',
        'single_weak': 'Single Weak',
        'collaborative_strong': 'Collab Strong',
        'collaborative_mix': 'Collab Mix',
        'collaborative_weak': 'Collab Weak',
        'competitive_strong': 'Comp Strong',
        'competitive_mix': 'Comp Mix',
        'competitive_weak': 'Comp Weak'
    }
    
    colors = {
        'single_strong': '#2E7D32',
        'single_weak': '#81C784',
        'collaborative_strong': '#1565C0',
        'collaborative_mix': '#42A5F5',
        'collaborative_weak': '#90CAF9',
        'competitive_strong': '#C62828',
        'competitive_mix': '#EF5350',
        'competitive_weak': '#E57373'
    }
    
    # Setup del plot
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = np.arange(len(files_with_mean))
    width = 0.1
    group_spacing = 0.03
    
    current_offset = 0
    positions = {}
    
    # Calcola posizioni barre
    for group_idx, group in enumerate(experiment_groups):
        for exp_type in group:
            positions[exp_type] = current_offset
            current_offset += width
        if group_idx < len(experiment_groups) - 1:
            current_offset += group_spacing
            
    total_width = current_offset
    offset_adjustment = -total_width / 2
    
    # Calcola medie globali per la colonna MEAN
    global_means = {}
    for exp_type in positions.keys():
        vals = []
        for filename in files:
            if exp_type in aggregated_data[filename]:
                vals.append(aggregated_data[filename][exp_type])
        global_means[exp_type] = np.mean(vals) if vals else 0
    
    # Disegna le barre
    for exp_type, base_offset in positions.items():
        values = []
        for filename in files:
            values.append(aggregated_data[filename].get(exp_type, 0))
        values.append(global_means[exp_type])
        
        offset = base_offset + offset_adjustment
        bars = ax.bar(x + offset, values, width,
                      label=exp_labels.get(exp_type, exp_type),
                      color=colors.get(exp_type, '#666666'))
        
        # Evidenzia la colonna MEAN
        bars[-1].set_alpha(0.7)
        bars[-1].set_edgecolor('black')
        bars[-1].set_linewidth(1.5)
        
    # Imposta la scala logaritmica
    ax.set_yscale('log')
    
    # Aggiorna l'etichetta e il titolo
    ax.set_ylabel('Total Tokens (Log Scale)', fontweight='bold', fontsize=11)
    ax.set_title('Token Usage for File and Experiment', fontweight='bold', fontsize=13)
    
    # Etichette asse X
    clean_labels = [f.replace('.py', '') for f in files_with_mean]
    ax.set_xticks(x)
    ax.set_xticklabels(clean_labels, rotation=45, ha='right')
    
    # Importante: 'which="both"' mostra la griglia anche per le suddivisioni logaritmiche minori
    ax.grid(axis='y', alpha=0.3, which="both")
    
    # Linea separatrice per MEAN
    ax.axvline(x=len(files) - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # Legenda
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.05),
        ncol=4,
        fontsize=9,
        frameon=True
    )
    
    plt.subplots_adjust(bottom=0.25, left=0.1, right=0.95, top=0.9)
    
    # Salvataggio
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / 'token_usage_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Grafico salvato in: {output_file}")
    plt.show()

# Esecuzione
if __name__ == "__main__":
    print(f"Analisi token da: {INPUT_FOLDER}")
    experiments = load_experiments(INPUT_FOLDER)
    aggregated_data = aggregate_tokens(experiments)
    if aggregated_data:
        plot_token_usage(aggregated_data, OUTPUT_FOLDER)
    else:
        print("Nessun dato trovato.")