from duckduckgo_search import ddg
import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

# Gesuchte Sicherungstypen
keywords = [
    "FNQ-R", "FNM-15", "LP-CC", "LPJ", "KTK", "KTK-R",
    "ATM fuse", "ATMR fuse", "ATQR fuse", "ATDR fuse", "AJT fuse"
]

# Zusätzliche Suchphrasen für Käufer/Sucher
search_phrases = [
    "kaufen", "beschaffen", "beziehen", "bedarf an", "suchen", "benötigen",
    "need", "looking for", "purchase", "buy", "procure", "require", "request"
]

# Funktion: Suchbegriffe kombinieren und suchen
def search_leads():
    results = []
    for keyword in keywords:
        for phrase in search_phrases:
            query = f'{keyword} {phrase} site:.de'
            print(f"🔍 Suche: {query}")
            try:
                search_results = ddg(query, max_results=10)
                if search_results:
                    for result in search_results:
                        url = result.get("href") or result.get("url")
                        title = result.get("title", "")
                        snippet = result.get("body", "")
                        if url and "verkauf" not in snippet.lower():
                            results.append({
                                "keyword": keyword,
                                "phrase": phrase,
                                "title": title,
                                "snippet": snippet,
                                "url": url
                            })
            except Exception as e:
                print(f"Fehler bei der Suche: {e}")
    return results

# Funktion: Ergebnisse speichern
def save_results(results):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"leads_{date}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "phrase", "title", "snippet", "url"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"💾 Ergebnisse gespeichert in {filename}")

# Hauptprogramm
if __name__ == "__main__":
    leads = search_leads()
    if leads:
        save_results(leads)
    else:
        print("Keine passenden Leads gefunden.")
