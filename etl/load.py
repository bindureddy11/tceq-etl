# etl/load.py
import json
import os

def save_to_json(data, output_path="output/proposed_rules.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)