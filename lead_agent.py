from duckduckgo_search import ddg
import requests
from bs4 import BeautifulSoup

# Sicherungstypen
fuse_types = ["FNM-15", "FNQ-R", "LP-CC", "LPJ", "KTK", "KTK-R", "ATM", "ATMR", "ATQR", "ATDR", "AJT"]

# Suchphrasen für Käufer
search_terms = []
for fuse in fuse_types:
    search_terms += [
        f'"wir suchen {fuse} Sicherungen site:.de"',
        f'"Bedarf an {fuse} Sicherung site:.de"',
        f'"Anfrage {fuse} Sicherung site:.de"',
        f'"benötigen {fuse} Sicherung site:.de"',
        f'"Sicherung {fuse} gesucht site:.de"',
        f'"Lieferant für {fuse} Sicherungen gesucht site:.de"',
        f'"Suche nach {fuse} Sicherungen site:.de"',
        f'"{fuse} Sicherung dringend benötigt site:.de"'
    ]

# Blacklist: typische Wörter für Verkäufer
blacklist_keywords = [
    "verkaufen", "distributor", "lieferant", "shop", "onlineshop", "vertrieb", "händler",
    "anbieten", "jetzt kaufen", "preis ab", "lagernd", "vorrätig", "zum verkauf", "angebot", "produkte"
]

def is_potential_buyer(url):
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, "html.parser")
        content = soup.get_text().lower()
        return not any(bad in content for bad in blacklist_keywords)
    except:
        return False

found_leads = []

# Durchsuche DuckDuckGo für alle Begriffe
for term in search_terms:
    print(f"🔎 Suche nach: {term}")
    results = ddg(term, region='de-de', safesearch='off', max_results=10)
    if results:
        for r in results:
            url = r['href']
            if is_potential_buyer(url) and url not in found_leads:
                found_leads.append(url)

# Ausgabe
print("\n✅ Gefundene potenzielle Käufer-Seiten:")
for lead in found_leads:
    print(lead)
