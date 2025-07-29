# etl/transform.py
import requests
import pdfplumber
import logging
from io import BytesIO
from etl.config import PDF_PAGES_TO_EXTRACT, PDF_REQUEST_TIMEOUT

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
    processed = 0
    skipped = 0
    failed = 0
    for url in pdf_urls:
        try:
            # Download the PDF file
            response = requests.get(url, timeout=PDF_REQUEST_TIMEOUT)
            response.raise_for_status()
            # Open the PDF from bytes
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                if not pdf.pages:
                    logger.warning(f"PDF at {url} has no pages.")
                    skipped += 1
                    continue
                # Extract text from the first two pages for easy view
                page_found = False
                pages = pdf.pages if PDF_PAGES_TO_EXTRACT is None else pdf.pages[:PDF_PAGES_TO_EXTRACT]
                for page in pages: 
                    page_text = page.extract_text()
                    if page_text:
                        combined_text += page_text + "\n"
                        page_found = True
                    else:
                        logger.info(f"Page in {url} has no extractable text.")
                if page_found:
                    processed += 1
                else:
                    skipped += 1
        except Exception as e:
            logger.error(f"PDF extraction failed for {url}: {e}")
            failed += 1
            continue
    logger.info(f"Processed {processed} PDFs, skipped {skipped}, failed {failed}.")
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
