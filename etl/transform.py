# etl/transform.py
import requests
import pdfplumber
from io import BytesIO

def extract_text_from_pdfs(pdf_urls):
    combined_text = ""
    for url in pdf_urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        combined_text += page_text + "\n"
        except Exception as e:
            print(f"Failed to extract from {url}: {e}")
            continue
    return combined_text.strip()

def enrich_rules_with_full_text(rules):
    for rule in rules:
        chapter_links = rule.get("chapter_links", [])
        full_text = extract_text_from_pdfs(chapter_links)
        rule["full_text"] = full_text
        del rule["chapter_links"]  # cleanup internal field
    return rules
