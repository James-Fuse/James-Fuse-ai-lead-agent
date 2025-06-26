# lead_agent/kleinanzeigen_checker.py

import requests
from bs4 import BeautifulSoup
from lead_agent.config import SEARCH_TERMS

def search_kleinanzeigen():
    base_url = "https://www.kleinanzeigen.de/s-anzeige:angebote.html"
    matches = []

    for term in SEARCH_TERMS:
        url = f"https://www.kleinanzeigen.de/s-suchanfrage.html?keywords={term.replace(' ', '+')}"
        response = requests.get(url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for result in soup.select("article.aditem"):
            title_tag = result.find("a", class_="ellipsis")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.kleinanzeigen.de" + title_tag["href"]
                matches.append(f"{title}\n{link}")

    return matches
