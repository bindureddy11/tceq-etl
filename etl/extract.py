# etl/extract.py
import requests
import logging
from bs4 import BeautifulSoup
from dateparser import parse as parse_date
from urllib.parse import urljoin
from etl.config import TCEQ_PROPOSED_RULES_URL, BASE_STATE_URL, MIN_ROW_CELLS, AGENCY_NAME

logger = logging.getLogger(__name__)

def extract_proposal_rules():
    """
    Scrapes the TCEQ proposed rules page for regulation metadata.
    Returns:
        list: A list of dictionaries, each containing metadata for a proposed rule.
    """

    url = TCEQ_PROPOSED_RULES_URL
    try:
        # Fetch the web page with a timeout
        r = requests.get(url,timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching url {url}: {e}")
        return []
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.content, "lxml")
    # Find the table containing proposed rules
    table = soup.find("table", class_="table table-striped")
    if not table:
        logger.warning("Could not find the rules table.")
        return []
    
    rules = []
    if table:
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            th = row.find("th", scope="row")

             # Skip rows that don't have the expected structure
            if not th or len(cells) < MIN_ROW_CELLS:
                continue

            # Extract proposed date and comments due from the first cell
            date_items = th.find_all("li")
            proposed_date = comments_due = comment_link = None
            
            for li in date_items:
                text = li.get_text(strip=True)
                a_tag = li.find("a", href=True)
                
                try:
                    if "Approval Date" in text:
                        # Parse proposed date and convert to string
                        proposed_date = str(parse_date(text.split(":", 1)[-1].strip()))
                    elif "Comments Due" in text:
                        # Parse comments_due date and convert to string
                        comments_due = str(parse_date(text.split(":", 1)[-1].strip()))
                    elif a_tag and "commentinput" in a_tag["href"]:  # Match by domain or pattern
                        # Extract comment link
                        comment_link = a_tag["href"]
                except Exception as e:
                    logger.error(f"Error parsing date from text '{text}': {e}")
                    continue                          

            # Extract identifier and title from the cells 
            identifier = cells[0].get_text(strip=True)
            title_cell = cells[1]

            title_tag = title_cell.find("span")
            title = title_tag.get_text(strip=True) if title_tag else ""
            # If title is empty, use the text directly from the cell
            if not title:
                title = title_cell.get_text(strip=True)

            # Description follows <br>, which becomes part of the next sibling text
            br_tag = title_cell.find("br")
            description = ""
            if br_tag and br_tag.next_sibling:
                description = br_tag.next_sibling.strip()   
           
            base_url = BASE_STATE_URL
            source_links = []
            chapters = []
            chapters_link = []
            link_items = cells[2].find_all("a", href=True)

            # Extract links and chapter information
            for link_tag in link_items:
                link_text = link_tag.get_text(strip=True)
                full_url = urljoin(base_url, link_tag["href"])
                source_links.append(full_url)
                if link_text.startswith("Ch."):
                    chapters.append(link_text)
                    chapters_link.append(full_url)
            
            

            # Create a rule dictionary with the extracted data
            rule = {
                "title": title,
                "identifier": identifier,
                "proposed_date": proposed_date,
                "comments_due": comments_due,
                "description": description,
                "chapters": chapters,
                "sources": source_links,
                "agency" : AGENCY_NAME,
                "chapter_links": chapters_link,  # pass to transformation 
                "comment_link": comment_link  
            }

            rules.append(rule)

    return rules
