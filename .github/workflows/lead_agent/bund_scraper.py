# lead_agent/bund_scraper.py

import requests
from bs4 import BeautifulSoup
from lead_agent.config import SEARCH_TERMS

def search_bund():
    base_url = "https://www.bund.de/DE/suche/suche_node.html"
    matches = []

    for term in SEARCH_TERMS:
        params = {"query": term}
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for result in soup.find_all("li", class_="search-entry"):
            title_tag = result.find("a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.bund.de" + title_tag["href"]
                matches.append(f"{title}\n{link}")

    return matches
