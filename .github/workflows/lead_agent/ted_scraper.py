# lead_agent/ted_scraper.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lead_agent import config, email_reporter

def search_ted():
    keywords = config.SEARCH_TERMS
    found_items = []

    for term in keywords:
        print(f"🔍 Searching TED for: {term}")
        url = f"https://ted.europa.eu/TED/search/search.do?queryText={term}&page=1"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"⚠️ HTTP {response.status_code} when accessing TED")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("div", class_="result-item")

            for res in results[:5]:  # Max. 5 Ergebnisse pro Suchwort
                title = res.find("a")
                date = res.find("span", class_="date")
                link = "https://ted.europa.eu" + title['href'] if title else ""
                text = title.text.strip() if title else "No title"
                date_str = date.text.strip() if date else "No date"

                found_items.append(f"{text} ({date_str})\n{link}\n")

        except Exception as e:
            print(f"❌ Error searching TED: {e}")

    if found_items:
        body = "Neue TED-Einträge mit Bezug zu Sicherungen:\n\n" + "\n\n".join(found_items)
        subject = f"🔔 {len(found_items)} neue TED-Treffer für Sicherungen ({datetime.now().date()})"
        email_reporter.send_email(subject, body)
    else:
        print("ℹ️ Keine TED-Ergebnisse gefunden.")
