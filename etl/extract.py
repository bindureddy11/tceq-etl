# etl/extract.py
import requests
import re
from bs4 import BeautifulSoup
from dateparser import parse as parse_date
from urllib.parse import urljoin

def extract_proposal_rules():
    """
    Scrapes the TCEQ proposed rules page for regulation metadata.
    Returns:
        list: A list of dictionaries, each containing metadata for a proposed rule.
    """

    url = "https://www.tceq.texas.gov/rules/prop.html"
    try:
        # Fetch the web page with a timeout
        r = requests.get(url,timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching url {url}: {e}")
        return []
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.content, "lxml")
    # Find the table containing proposed rules
    table = soup.find("table", class_="table table-striped")
    if not table:
        print("Warning: Could not find the rules table.")
        return []
    
    rules = []
    if table:
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            th = row.find("th", scope="row")

             # Skip rows that don't have the expected structure
            if not th or len(cells) < 3:
                continue

            # Extract proposed date and comments due from the first cell
            date_items = th.find_all("li")
            proposed_date = comments_due = None

            for li in date_items:
                text = li.get_text(strip=True)
                try:
                    if "Approval Date" in text:
                        # Parse proposed date and convert to string
                        proposed_date = str(parse_date(text.split(":", 1)[-1].strip()))
                    elif "Comments Due" in text:
                        # Parse comments_due date and convert to string
                        comments_due = str(parse_date(text.split(":", 1)[-1].strip()))
                except Exception as e:
                    print(f"Error parsing date from text '{text}': {e}")
                    continue

            # Extract identifier and title from the cells 
            identifier = cells[0].get_text(strip=True)
            title = cells[1].get_text(strip=True)

            base_url = "https://www.tceq.texas.gov"
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
                "chapters": chapters,
                "sources": source_links,
                "chapter_links": chapters_link  # pass to transformation
            }

            rules.append(rule)

    return rules
