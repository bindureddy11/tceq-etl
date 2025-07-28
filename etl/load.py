# etl/load.py
import json
import os
import logging

logger = logging.getLogger(__name__)

def save_to_json(data, output_path="output/proposed_rules.json"):
    """
    Saves the provided data as a JSON file to the specified output path.

    Args:
        data (object): The data to be saved (typically a list or dict).
        output_path (str): The file path where the JSON will be saved.

    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Write the data to a JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data successfully saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving data to {output_path}: {e}")