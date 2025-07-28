# etl/transform.py
import requests
import pdfplumber
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

def extract_text_from_pdfs(pdf_urls):
    """
    Downloads and extracts text from the first two pages of each PDF in the provided URLs.

    Args:
        pdf_urls (list): List of URLs pointing to PDF files.

    Returns:
        str: Combined extracted text from all PDFs.
    """
    combined_text = ""
    for url in pdf_urls:
        try:
            # Download the PDF file
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            # Open the PDF from bytes
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                if not pdf.pages:
                    logger.warning(f"PDF at {url} has no pages.")
                    continue
                # Extract text from the first two pages for performance
                for page in pdf.pages[:2]: 
                    page_text = page.extract_text()
                    if page_text:
                        combined_text += page_text + "\n"
                    else:
                        logger.info(f"Page in {url} has no extractable text.")
        except Exception as e:
            logger.error(f"PDF extraction failed for {url}: {e}")
            continue
    return combined_text.strip()

def enrich_rules_with_full_text(rules):
    """
    For each rule, downloads and extracts full text from its chapter PDF links,
    then adds the extracted text to the rule dictionary.

    Args:
        rules (list): List of rule dictionaries, each with a 'chapter_links' key.

    Returns:
        list: The same list of rules, each with an added 'full_text' field.
    """
    for rule in rules:
        chapter_links = rule.get("chapter_links", [])
        full_text = extract_text_from_pdfs(chapter_links)
        rule["full_text"] = full_text
        del rule["chapter_links"]  # cleanup internal field
    return rules
