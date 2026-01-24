#!/usr/bin/env python3
"""
Script to extract code from input.jsonl and create individual files
in the new_dataset folder.
"""
import json
import os
from pathlib import Path

# Configuration
INPUT_FILE = "dataset_generation/input.jsonl"
OUTPUT_DIR = "data/input_code"

def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Read the JSONL file
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            # Parse each JSON line
            entry = json.loads(line.strip())
            
            # Extract task_id and code
            task_id = entry.get('task_id')
            code = entry.get('code', '')
            
            if task_id is None:
                print(f"Warning: Entry without task_id found, skipping...")
                continue
            
            # Create filename: t<task_id>.py
            filename = f"t{task_id}.py"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Write code to file
            with open(filepath, 'w', encoding='utf-8') as code_file:
                code_file.write(code)
            
            print(f"Created: {filepath}")
    
    print(f"\nDone! All files created in '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    main()
