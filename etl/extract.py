# etl/extract.py
import logging
import requests
from bs4 import BeautifulSoup
from dateparser import parse as parse_date
from urllib.parse import urljoin
from etl.config import (
    TCEQ_PROPOSED_RULES_URL,
    BASE_STATE_URL,
    MIN_ROW_CELLS,
    AGENCY_NAME,
    PDF_REQUEST_TIMEOUT
)

logger = logging.getLogger(__name__)

# Fetches HTML content from the given URL
def fetch_html(url):
    try:
        response = requests.get(url, timeout=PDF_REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None

# Parses date fields and comment submission link from <li> elements
def parse_dates_and_comment_link(date_items):
    proposed_date = comments_due = comment_link = None
    for li in date_items:
        text = li.get_text(strip=True)
        a_tag = li.find("a", href=True)
        try:
            if "Approval Date" in text:
                proposed_date = str(parse_date(text.split(":", 1)[-1].strip()))
            elif "Comments Due" in text:
                comments_due = str(parse_date(text.split(":", 1)[-1].strip()))
            elif a_tag and "commentinput" in a_tag["href"]:
                comment_link = a_tag["href"]
        except Exception as e:
            logger.error(f"Error parsing date from '{text}': {e}")
            continue
    return proposed_date, comments_due, comment_link

# Extracts chapter and source document links from the table cell
def extract_links_and_chapters(cell):
    source_links = []
    chapters = []
    chapters_link = []
    link_items = cell.find_all("a", href=True)
    for link_tag in link_items:
        link_text = link_tag.get_text(strip=True)
        full_url = urljoin(BASE_STATE_URL, link_tag["href"])
        source_links.append(full_url)
        if link_text.startswith("Ch."):
            chapters.append(link_text)
            chapters_link.append(full_url)
    return source_links, chapters, chapters_link

# Main function to extract rule metadata from TCEQ proposed rules page
def extract_proposal_rules():
    """
    Scrapes the TCEQ proposed rules page for regulation metadata.
    Returns:
        list: A list of dictionaries, each containing metadata for a proposed rule.
    """

    # Step 1: Fetch HTML from the proposed rules page
    html_content = fetch_html(TCEQ_PROPOSED_RULES_URL)
    if not html_content:
        return []

    # Step 2: Parse HTML using BeautifulSoup
    try:
        soup = BeautifulSoup(html_content, "lxml")
    except Exception as e:
        logger.error(f"Error parsing HTML with BeautifulSoup: {e}")
        return []

    # Step 3: Locate the rules table
    table = soup.find("table", class_="table table-striped")
    if not table:
        logger.warning("Could not find the rules table.")
        return []

    # Step 4: Extract table body and rows
    try:
        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if tbody else []
        if not rows:
            logger.warning("No <tr> rows found in the <tbody> of the rules table.")
            return []
    except Exception as e:
        logger.error(f"Error accessing table structure: {e}")
        return []

    rules = []

    # Step 5: Process each row
    for row in rows:
        try:
            cells = row.find_all("td")
            th = row.find("th", scope="row")

            # Skip malformed rows
            if not th or len(cells) < MIN_ROW_CELLS:
                continue

            # Extract identifier and title
            identifier = cells[0].get_text(strip=True)
            title_cell = cells[1]
            title_tag = title_cell.find("span")
            title = title_tag.get_text(strip=True) if title_tag else title_cell.get_text(strip=True)

            # Extract description from the <br> tag's next sibling
            br_tag = title_cell.find("br")
            description = br_tag.next_sibling.strip() if br_tag and br_tag.next_sibling else ""

            # Extract proposed date, comments due, and comment link
            date_items = th.find_all("li")
            proposed_date, comments_due, comment_link = parse_dates_and_comment_link(date_items)

            # Extract document/chapter links from third cell
            source_links, chapters, chapters_link = extract_links_and_chapters(cells[2])

            # Create structured rule dictionary
            rule = {
                "title": title,
                "identifier": identifier,
                "proposed_date": proposed_date,
                "comments_due": comments_due,
                "description": description,
                "chapters": chapters,
                "sources": source_links,
                "agency": AGENCY_NAME,
                "chapter_links": chapters_link,
                "comment_link": comment_link
            }

            rules.append(rule)

        except Exception:
            logger.exception("Error processing a row")
            continue

    # Step 6: Return all collected rule dictionaries
    return rules
