from etl.extract import extract_proposal_rules
from etl.transform import enrich_rules_with_full_text
from etl.load import save_to_json

def main():
    """
    Orchestrates the ETL pipeline:
    1. Extracts proposed rules from the TCEQ website.
    2. Enriches each rule with full text extracted from linked PDFs.
    3. Saves the enriched data as JSON to the output directory.
    """
    
    print(" Extracting rules...")
    rules = extract_proposal_rules()
    if not rules:
        print("No rules extracted. Exiting.")
        return
    print("Enriching with full text from PDFs...")

    # Warn if no rules contain full text
    enriched_rules = enrich_rules_with_full_text(rules)
    if not any(rule.get("full_text") for rule in enriched_rules):
        print("Warning: No rules contain full_text.")

    print("Saving to output/proposed_rules.json...")
    save_to_json(enriched_rules)
    print("Done.")

if __name__ == "__main__":
    main()
