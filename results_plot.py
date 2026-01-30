#!/usr/bin/env python3
"""
Script per generare grafici da esperimenti di test automation
Analizza file JSON e crea grafici comparativi per coverage e mutation score
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
IGNORED_FILES = [
    # 'complex_logic.py',
    #'d01_bank_account.py',
    #"d03_stack.py",
    # 'd04_linked_list.py',
]

# ============================================================================


def classify_experiment(experiment_name):
    """
    Classifica l'esperimento in base al nome
    Ritorna: (mode, strength) dove mode = 'single'|'collaborative'|'competitive'
    e strength = 'strong'|'weak'|'mix'
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
    
    # Conta i modelli
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
    """
    Carica tutti i file JSON dalla cartella di input
    Ritorna un dizionario strutturato per tipo di esperimento
    """
    experiments = defaultdict(lambda: defaultdict(list))
    
    input_path = Path(input_folder)
    if not input_path.exists():
        print(f"Errore: la cartella {input_folder} non esiste")
        sys.exit(1)
    
    json_files = list(input_path.glob('*.json'))
    if not json_files:
        print(f"Errore: nessun file JSON trovato in {input_folder}")
        sys.exit(1)
    
    print(f"Trovati {len(json_files)} file JSON")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            experiment_name = data.get('experiment_name', '')
            mode, strength = classify_experiment(experiment_name)
            
            if mode and strength:
                print(f"  {json_file.name}: {mode} {strength}")
                experiments[mode][strength].append(data)
            else:
                print(f"  {json_file.name}: tipo non riconosciuto, saltato")
                
        except Exception as e:
            print(f"Errore nel leggere {json_file}: {e}")
    
    return experiments


def aggregate_metrics(experiments):
    """
    Aggrega le metriche per file e tipo di esperimento
    Ritorna: dict[file][experiment_type] = {'coverage': avg, 'mutation': avg}
    """
    aggregated = defaultdict(lambda: defaultdict(lambda: {'coverage': [], 'mutation': []}))
    
    # Tipi di esperimento nell'ordine desiderato
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
                    
                    # Ignora i file specificati nella configurazione
                    if filename in IGNORED_FILES:
                        continue
                    
                    metrics = result.get('metrics', {})
                    
                    exp_type = f"{mode}_{strength}"
                    aggregated[filename][exp_type]['coverage'].append(
                        metrics.get('coverage_percent', 0)
                    )
                    aggregated[filename][exp_type]['mutation'].append(
                        metrics.get('mutation_score_percent', 0)
                    )
    
    # Calcola le medie
    final_data = defaultdict(dict)
    for filename in aggregated:
        for exp_type in aggregated[filename]:
            coverage_values = aggregated[filename][exp_type]['coverage']
            mutation_values = aggregated[filename][exp_type]['mutation']
            
            final_data[filename][exp_type] = {
                'coverage': np.mean(coverage_values) if coverage_values else 0,
                'mutation': np.mean(mutation_values) if mutation_values else 0,
                'count': len(coverage_values)
            }
    
    return final_data


def plot_metrics(aggregated_data, output_folder):
    """
    Crea i grafici per coverage e mutation score con spaziatura tra i gruppi
    """
    # Ordine dei file (ordinamento alfabetico)
    
    # Sort files: dNN files first (sorted), then complex_file last
    dnn_files = sorted([f for f in aggregated_data.keys() if f.startswith('d') and f[1:3].isdigit()])
    other_files = sorted([f for f in aggregated_data.keys() if not (f.startswith('d') and f[1:3].isdigit())])
    files = dnn_files + other_files
    
    # Aggiungi "MEAN" come ultima posizione
    files_with_mean = files + ['MEAN']
    
    # Tipi di esperimento raggruppati
    experiment_groups = [
        ['single_strong', 'single_weak'],
        ['collaborative_strong', 'collaborative_mix', 'collaborative_weak'],
        ['competitive_strong', 'competitive_mix', 'competitive_weak']
    ]
    
    # Labels più leggibili
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
    
    # Colori per ogni tipo
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
    
    # Crea figura con 2 subplot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    x = np.arange(len(files_with_mean))
    width = 0.1  # Larghezza delle barre
    group_spacing = 0.03  # Spaziatura tra i gruppi
    
    # Calcola le posizioni con spaziatura tra gruppi
    current_offset = 0
    positions = {}
    
    for group_idx, group in enumerate(experiment_groups):
        for i, exp_type in enumerate(group):
            positions[exp_type] = current_offset
            current_offset += width
        # Aggiungi spaziatura dopo ogni gruppo (tranne l'ultimo)
        if group_idx < len(experiment_groups) - 1:
            current_offset += group_spacing
    
    # Centra le barre rispetto alla posizione x
    total_width = current_offset
    offset_adjustment = -total_width / 2
    
    # Calcola i valori medi per ogni tipo di esperimento
    mean_coverage = {}
    mean_mutation = {}
    for exp_type in positions.keys():
        coverage_vals = []
        mutation_vals = []
        for filename in files:
            if exp_type in aggregated_data[filename]:
                coverage_vals.append(aggregated_data[filename][exp_type]['coverage'])
                mutation_vals.append(aggregated_data[filename][exp_type]['mutation'])
        mean_coverage[exp_type] = np.mean(coverage_vals) if coverage_vals else 0
        mean_mutation[exp_type] = np.mean(mutation_vals) if mutation_vals else 0
    
    # Plot Coverage
    for exp_type, base_offset in positions.items():
        coverage_values = []
        for filename in files:
            value = aggregated_data[filename].get(exp_type, {}).get('coverage', 0)
            coverage_values.append(value)
        # Aggiungi il valore medio alla fine
        coverage_values.append(mean_coverage[exp_type])
        
        offset = base_offset + offset_adjustment
        bars = ax1.bar(x + offset, coverage_values, width, 
                label=exp_labels.get(exp_type, exp_type),
                color=colors.get(exp_type, '#666666'))
        
        # Rendi la barra MEAN più scura
        bars[-1].set_alpha(0.7)
        bars[-1].set_edgecolor('black')
        bars[-1].set_linewidth(1.5)
    
    # ax1.set_xlabel('File', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Coverage %', fontweight='bold', fontsize=11)
    ax1.set_title('Test Coverage', fontweight='bold', fontsize=13)
    ax1.set_xticks(x)
    ax1.set_xticklabels(files_with_mean, rotation=45, ha='right')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim(0, 105)
    
    # Aggiungi una linea verticale prima di MEAN per separarlo
    ax1.axvline(x=len(files) - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # Plot Mutation Score
    for exp_type, base_offset in positions.items():
        mutation_values = []
        for filename in files:
            value = aggregated_data[filename].get(exp_type, {}).get('mutation', 0)
            mutation_values.append(value)
        # Aggiungi il valore medio alla fine
        mutation_values.append(mean_mutation[exp_type])
        
        offset = base_offset + offset_adjustment
        bars = ax2.bar(x + offset, mutation_values, width,
                label=exp_labels.get(exp_type, exp_type),
                color=colors.get(exp_type, '#666666'))
        
        # Rendi la barra MEAN più scura
        bars[-1].set_alpha(0.7)
        bars[-1].set_edgecolor('black')
        bars[-1].set_linewidth(1.5)
    
    # ax2.set_xlabel('File', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Mutation Score %', fontweight='bold', fontsize=11)
    ax2.set_title('Mutation Score', fontweight='bold', fontsize=13)
    ax2.set_xticks(x)
    ax2.set_xticklabels(files_with_mean, rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(0, 105)
    
    # Aggiungi una linea verticale prima di MEAN per separarlo
    ax2.axvline(x=len(files) - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.subplots_adjust(bottom=0.25, hspace=0.6, left=0.1, right=0.95, top=0.95)

    # La legenda va spostata ancora più in basso dato che abbiamo alzato il margine bottom
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(
        handles, 
        labels,
        loc='lower center', 
        bbox_to_anchor=(0.5, 0.02), # Alzato leggermente rispetto al bordo assoluto
        ncol=4,
        fontsize=9,
        frameon=True
    )

    # Aggiungi legenda fuori dal grafico (in basso al centro)
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(
        handles, 
        labels,
        loc='lower center', 
        bbox_to_anchor=(0.5, -0.05), 
        ncol=4,
        fontsize=9,
        frameon=True
    )
    
    # Salva il grafico
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    output_file = output_path / 'experiment_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nGrafico salvato in: {output_file}")
    
    plt.show()


def print_summary(aggregated_data):
    """
    Stampa un riepilogo dei dati
    """
    print("\n" + "="*80)
    print("RIEPILOGO DATI")
    print("="*80)
    
    for filename in sorted(aggregated_data.keys()):
        print(f"\n{filename}:")
        for exp_type in sorted(aggregated_data[filename].keys()):
            data = aggregated_data[filename][exp_type]
            print(f"  {exp_type:25s} - Coverage: {data['coverage']:6.2f}% | "
                  f"Mutation: {data['mutation']:6.2f}% | Samples: {data['count']}")


def main():
    """
    Funzione principale
    """
    print(f"Caricamento esperimenti da: {INPUT_FOLDER}")
    experiments = load_experiments(INPUT_FOLDER)
    
    if IGNORED_FILES:
        print(f"\nFile ignorati: {', '.join(IGNORED_FILES)}")
    
    print(f"\nAggregazione metriche...")
    aggregated_data = aggregate_metrics(experiments)
    
    if not aggregated_data:
        print("Errore: nessun dato da visualizzare")
        sys.exit(1)
    
    print_summary(aggregated_data)
    
    print(f"\nGenerazione grafici...")
    plot_metrics(aggregated_data, OUTPUT_FOLDER)
    
    print("\n✓ Completato!")


if __name__ == '__main__':
    main()
