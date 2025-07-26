# etl/extract.py
import requests
import re
from bs4 import BeautifulSoup
from dateparser import parse as parse_date
from urllib.parse import urljoin


def extract_proposal_rules():
    url = "https://www.tceq.texas.gov/rules/prop.html"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")
    table = soup.find("table", class_="table table-striped")
    rules = []

    if table:
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            th = row.find("th", scope="row")
            
            if not th or len(cells) < 3:
                continue

            date_items = th.find_all("li")
            proposed_date = comments_due = None

            for li in date_items:
                text = li.get_text(strip=True)
                if "Approval Date" in text:
                    proposed_date = str(parse_date(text.split(":", 1)[-1].strip()))
                elif "Comments Due" in text:
                    comments_due = str(parse_date(text.split(":", 1)[-1].strip()))

            identifier = cells[0].get_text(strip=True)
            title = cells[1].get_text(strip=True)

            base_url = "https://www.tceq.texas.gov"
            source_links = []
            chapters = []
            chapters_link = []
            link_items = cells[2].find_all("a", href=True)

            for link_tag in link_items:
                link_text = link_tag.get_text(strip=True)
                full_url = urljoin(base_url, link_tag["href"])
                source_links.append(full_url)
                if link_text.startswith("Ch."):
                    chapters.append(link_text)
                    chapters_link.append(full_url)

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
