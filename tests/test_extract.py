import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.extract import extract_proposal_rules

def test_extract_non_empty_proposal_rules():
    rules = extract_proposal_rules()
    assert len(rules) > 0, "No rules were extracted"
    
    for rule in rules:
        assert "title" in rule, "Each rule should have a title"
        assert "identifier" in rule, "Each rule should have a identifier"
        assert "proposed_date" in rule, "Each rule should have a proposed_date"
        assert len(rule["chapter_links"]) > 0, "Chapter links should not be empty"
