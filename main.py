from etl.extract import extract_proposal_rules
from etl.transform import enrich_rules_with_full_text
from etl.load import save_to_json

def main():
    print(" Extracting rules...")
    rules = extract_proposal_rules()

    print("Enriching with full text from PDFs...")
    enriched_rules = enrich_rules_with_full_text(rules)

    print("Saving to output/proposed_rules.json...")
    save_to_json(enriched_rules)
    print("Done.")

if __name__ == "__main__":
    main()
