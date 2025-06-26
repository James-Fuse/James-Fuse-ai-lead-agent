# lead_agent/website_crawler.py

import requests
from bs4 import BeautifulSoup
from lead_agent.config import SEARCH_TERMS

def search_industrystock():
    base_url = "https://www.industrystock.de"
    matches = []

    for term in SEARCH_TERMS:
        query = term.replace(" ", "+")
        url = f"{base_url}/Search?searchword={query}"
        response = requests.get(url)

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("div.media-body h3 a")

        for r in results:
            title = r.get_text(strip=True)
            link = base_url + r["href"]
            matches.append(f"{title}\n{link}")

    return matches
