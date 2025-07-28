import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.transform import extract_text_from_pdfs

def test_extract_text_from_pdfs():
    sample_url = "https://www.tceq.texas.gov/downloads/rules/current/25006115_pro.pdf"
    text = extract_text_from_pdfs([sample_url])
    assert len(text.strip()) > 50