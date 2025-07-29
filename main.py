import os
import time
import logging
from etl.extract import extract_proposal_rules
from etl.transform import enrich_rules_with_full_text
from etl.load import save_to_json
from etl.config import LOG_DIR, LOG_FILE_PATH

os.makedirs(LOG_DIR, exist_ok=True)
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='a'), # Log to a file
        logging.StreamHandler() # Also log to console
    ]
)
def main():
    """
    Orchestrates the ETL pipeline:
    1. Extracts proposed rules from the TCEQ website.
    2. Enriches each rule with full text extracted from linked PDFs.
    3. Saves the enriched data as JSON to the output directory.
    """
    start_time = time.time()  # Start timer

    logging.info("Extracting rules...")
    rules = extract_proposal_rules()
    if not rules:
        logging.info("No rules extracted. Exiting.")
        return
    
    logging.info("Enriching with full text from PDFs...")
    # Warn if no rules contain full text
    enriched_rules = enrich_rules_with_full_text(rules)
    if not any(rule.get("full_text") for rule in enriched_rules):
        logging.info("Warning: No rules contain full_text.")

    logging.info("Saving to output/proposed_rules.json...")
    save_to_json(enriched_rules)
    logging.info("Done.")

    elapsed = time.time() - start_time  # End timer
    logging.info(f"Total pipeline run time: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
