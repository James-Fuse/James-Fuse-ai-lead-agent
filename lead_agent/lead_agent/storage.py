import csv
from typing import List, Dict

def write_csv(leads: List[Dict], path: str) -> None:
    if not leads:
        return
    # Spaltennamen automatisch aus allen Dict-Keys sammeln
    fieldnames = sorted({k for lead in leads for k in lead.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
