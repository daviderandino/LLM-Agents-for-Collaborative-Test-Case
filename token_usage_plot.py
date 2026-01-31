#!/usr/bin/env python3
"""
Script per generare grafici del consumo di token da esperimenti di test automation.
Analizza file JSON, calcola le medie e crea grafici comparativi con scala logaritmica.
Utilizza le etichette specifiche: Planner+, Worker+, ecc.
"""

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

# Cartelle di input e output
INPUT_FOLDER = './results'
OUTPUT_FOLDER = './graphs'

# File da ignorare (non saranno inclusi nei grafici)
IGNORED_FILES = []

# ============================================================================

def classify_experiment(experiment_name):
    """
    Classifica l'esperimento in base al nome.
    Ritorna: (mode, strength)
    """
    name_lower = experiment_name.lower()
    
    if 'collaborative' in name_lower:
        mode = 'collaborative'
    elif 'competitive' in name_lower:
        mode = 'competitive'
    elif 'single' in name_lower:
        mode = 'single'
    else:
        return None, None
    
    strong_models = ['gptoss120b', 'llama70b']
    weak_models = ['gptoss20b', 'llama17b', 'llamascout17b']
    
    strong_count = sum(1 for model in strong_models if model in name_lower)
    weak_count = sum(1 for model in weak_models if model in name_lower)
    
    if mode == 'single':
        strength = 'strong' if strong_count > 0 else 'weak'
    else:
        if strong_count > 0 and weak_count == 0:
            strength = 'strong'
        elif weak_count > 0 and strong_count == 0:
            strength = 'weak'
        elif strong_count > 0 and weak_count > 0:
            strong_indices = [name_lower.find(m) for m in strong_models if m in name_lower]
            first_strong_idx = min(strong_indices) if strong_indices else float('inf')
            weak_indices = [name_lower.find(m) for m in weak_models if m in name_lower]
            first_weak_idx = min(weak_indices) if weak_indices else float('inf')
            
            if first_strong_idx < first_weak_idx:
                strength = 'strong_planner' # Strong model is first
            else:
                strength = 'strong_worker'  # Strong model is second
        else:
            strength = 'unknown'
    
    return mode, strength

def load_experiments(input_folder):
    experiments = defaultdict(lambda: defaultdict(list))
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Errore: la cartella {input_folder} non esiste")
        return experiments
    
    json_files = list(input_path.glob('*.json'))
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            mode, strength = classify_experiment(data.get('experiment_name', ''))
            if mode and strength:
                experiments[mode][strength].append(data)
        except Exception as e:
            print(f"Errore nel leggere {json_file}: {e}")
    return experiments

def aggregate_token_metrics(experiments):
    aggregated = defaultdict(lambda: defaultdict(list))
    # Ordine dei tipi basato sulla logica del primo script
    experiment_types = [
        ('single', 'strong'), ('single', 'weak'),
        ('collaborative', 'strong'), ('collaborative', 'strong_planner'),
        ('collaborative', 'strong_worker'), ('collaborative', 'weak'),
        ('competitive', 'strong'), ('competitive', 'strong_planner'),
        ('competitive', 'strong_worker'), ('competitive', 'weak')
    ]
    
    for mode, strength in experiment_types:
        if mode in experiments and strength in experiments[mode]:
            for exp_data in experiments[mode][strength]:
                for result in exp_data.get('results', []):
                    filename = result['file']
                    if filename in IGNORED_FILES: continue
                    exp_type = f"{mode}_{strength}"
                    aggregated[filename][exp_type].append(result.get('metrics', {}).get('total_tokens', 0))
    
    final_data = defaultdict(dict)
    for filename in aggregated:
        for exp_type in aggregated[filename]:
            token_values = aggregated[filename][exp_type]
            final_data[filename][exp_type] = {
                'tokens': np.mean(token_values) if token_values else 0,
                'count': len(token_values)
            }
    return final_data

def plot_tokens(aggregated_data, output_folder):
    # Ordinamento file (dNN prima, poi gli altri)
    dnn_files = sorted([f for f in aggregated_data.keys() if f[0:1].isdigit()])
    other_files = sorted([f for f in aggregated_data.keys() if not f[0:1].isdigit()])
    files = dnn_files + other_files
    files_with_mean = files + ['MEAN']
    
    # Gruppi di esperimento
    experiment_groups = [
        ['single_strong', 'single_weak'],
        ['collaborative_strong', 'collaborative_strong_planner', 'collaborative_strong_worker', 'collaborative_weak'],
        ['competitive_strong', 'competitive_strong_planner', 'competitive_strong_worker', 'competitive_weak']
    ]
    
    # Label originali dal primo script
    exp_labels = {
        'single_strong': 'Single Strong',
        'single_weak': 'Single Weak',
        'collaborative_strong': 'Collab Strong',
        'collaborative_strong_planner': 'Collab Planner+',
        'collaborative_strong_worker': 'Collab Worker+',
        'collaborative_weak': 'Collab Weak',
        'competitive_strong': 'Comp Strong',
        'competitive_strong_planner': 'Comp Planner+',
        'competitive_strong_worker': 'Comp Worker+',
        'competitive_weak': 'Comp Weak'
    }
    
    # Colori originali dal primo script
    colors = {
        'single_strong': '#2E7D32', 'single_weak': '#81C784',
        'collaborative_strong': '#0D47A1', 'collaborative_strong_planner': '#1976D2',
        'collaborative_strong_worker': '#64B5F6', 'collaborative_weak': '#BBDEFB',
        'competitive_strong': '#B71C1C', 'competitive_strong_planner': '#D32F2F',
        'competitive_strong_worker': '#E57373', 'competitive_weak': '#FFCDD2'
    }

    fig, ax = plt.subplots(figsize=(14, 10))
    x = np.arange(len(files_with_mean))
    width = 0.08 
    group_spacing = 0.03
    
    current_offset = 0
    positions = {}
    for group_idx, group in enumerate(experiment_groups):
        for i, exp_type in enumerate(group):
            positions[exp_type] = current_offset
            current_offset += width
        if group_idx < len(experiment_groups) - 1:
            current_offset += group_spacing
    
    total_width = current_offset
    offset_adjustment = -total_width / 2

    # Calcolo medie per la colonna MEAN
    mean_tokens = {}
    for exp_type in positions.keys():
        vals = []
        for f in files:
            if exp_type in aggregated_data[f]:
                vals.append(aggregated_data[f][exp_type]['tokens'])
        mean_tokens[exp_type] = np.mean(vals) if vals else 0

    # Generazione barre
    for exp_type, base_offset in positions.items():
        token_values = []
        for f in files:
            token_values.append(aggregated_data[f].get(exp_type, {}).get('tokens', 0))
        token_values.append(mean_tokens[exp_type])
        
        offset = base_offset + offset_adjustment
        bars = ax.bar(x + offset, token_values, width, 
                     label=exp_labels.get(exp_type, exp_type), 
                     color=colors.get(exp_type, '#666666'))
        
        # Stile per la colonna MEAN
        bars[-1].set_alpha(0.7)
        bars[-1].set_edgecolor('black')
        bars[-1].set_linewidth(1.5)

    # Configurazione Assi Logaritmici
    ax.set_yscale('log')
    ax.set_ylabel('Total Tokens (Log Scale)', fontweight='bold', fontsize=11)
    ax.set_title('Token Usage Comparison (Logarithmic Scale)', fontweight='bold', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(files_with_mean, rotation=45, ha='right')
    ax.grid(True, which="both", ls="-", alpha=0.3)
    ax.axvline(x=len(files) - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # Legenda e Layout
    plt.subplots_adjust(bottom=0.25)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), 
              ncol=5, fontsize=9, frameon=True, fancybox=True, shadow=True)
    
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path / 'token_usage_comparison_log.png', dpi=300, bbox_inches='tight')
    print(f"Grafico salvato in: {output_path / 'token_usage_comparison_log.png'}")
    plt.show()

def main():
    print(f"Caricamento dati da {INPUT_FOLDER}...")
    experiments = load_experiments(INPUT_FOLDER)
    aggregated_data = aggregate_token_metrics(experiments)
    
    if not aggregated_data:
        print("Errore: nessun dato da visualizzare")
        sys.exit(1)

    print("Generazione grafico con etichette originali e scala logaritmica...")
    plot_tokens(aggregated_data, OUTPUT_FOLDER)
    print("✓ Completato!")

if __name__ == '__main__':
    main()