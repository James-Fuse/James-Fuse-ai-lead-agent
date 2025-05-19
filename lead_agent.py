from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Alle Sicherungstypen, die gesucht werden sollen
fuse_types = ["FNM-15", "FNQ-R", "LP-CC", "LPJ", "KTK", "KTK-R", "ATM", "ATMR", "ATQR", "ATDR", "AJT"]

# Erstelle gezielte Suchphrasen für Käufer
search_terms = []
for fuse in fuse_types:
    search_terms += [
        f'"wir suchen {fuse} Sicherungen"',
        f'"Bedarf an {fuse} Sicherung"',
        f'"Anfrage {fuse} Sicherung"',
        f'"benötigen {fuse} Sicherung"',
        f'"Sicherung {fuse} gesucht"',
        f'"Lieferant für {fuse} Sicherungen gesucht"',
        f'"Suche nach {fuse} Sicherungen"',
        f'"{fuse} Sicherung dringend benötigt"'
    ]

# Keywords, die auf Verkäufer oder Shops hindeuten → diese Seiten werden ausgeschlossen
blacklist_keywords = [
    "verkaufen", "distributor", "lieferant", "shop", "onlineshop", "vertrieb", "händler",
    "anbieten", "jetzt kaufen", "preis ab", "lagernd", "vorrätig", "zum verkauf", "angebot", "produkte"
]

def is_potential_buyer(url):
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, "html.parser")
        content = soup.get_text().lower()
        
        # Wenn Seite Verkäufer-Vokabular enthält → ignorieren
        if any(bad in content for bad in blacklist_keywords):
            return False
        
        return True
    except:
        return False

found_leads = []

# Durchsuche Google für alle Begriffe
for term in search_terms:
    print(f"Suche nach: {term}")
    for url in search(term + " site:.de", num_results=10):
        if is_potential_buyer(url):
            if url not in found_leads:
                found_leads.append(url)

# Ausgabe
print("\nGefundene potenzielle Käufer-Seiten:")
for lead in found_leads:
    print(lead)

