import yaml
import os
from datetime import datetime

class ConfigManager:
    def __init__(self, experiment_file=None):
        self.config = self._load_yaml('configs/default.yaml')
        
        if experiment_file:
            print(f"🧪 Loading Experiment: {experiment_file}")
            overrides = self._load_yaml(experiment_file)
            self._merge_configs(self.config, overrides)

        # Create a unique ID for this run for result tracking
        self.experiment_name = os.path.splitext(os.path.basename(experiment_file or "default"))[0]
        
        # Generate run_id once at initialization
        self.run_id = self.experiment_name + '_' + datetime.now().isoformat(timespec="seconds")
        
        # Salva direttamente in results/ senza creare sottocartelle
        os.makedirs("results", exist_ok=True)

    def _load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _merge_configs(self, base, overrides):
        """Recursively merge dictionaries."""
        for key, value in overrides.items():
            if isinstance(value, dict) and key in base:
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def get(self, section, key):
        return self.config.get(section, {}).get(key)
        
    def save_snapshot(self):
        """Save the exact config used for this run into the results folder."""
        with open(os.path.join(self.results_dir, 'config_snapshot.yaml'), 'w') as f:
            yaml.dump(self.config, f)

# Usage Example:
# cfg = ConfigManager('configs/experiments/aggressive.yaml')
# temp = cfg.get('llm', 'temperature')