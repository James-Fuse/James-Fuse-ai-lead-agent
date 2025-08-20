import re
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict, Iterable, Set

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; James-Fuse-LeadAgent/1.0; +https://www.james-fuse.de)"
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s./-]?)?(?:\(?\d{2,4}\)?[\s./-]?)?\d{3,4}[\s./-]?\d{3,6}")

def load_targets(path: str = "targets.txt") -> List[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    except FileNotFoundError:
        return []

def fetch(url: str, timeout: int = 15) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if r.ok and "text/html" in r.headers.get("Content-Type", ""):
            return r.text
    except requests.RequestException:
        pass
    return ""

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return " ".join(soup.get_text(" ").split())

def find_emails(text: str) -> List[str]:
    return sorted(set(EMAIL_RE.findall(text)))

def find_phones(text: str) -> List[str]:
    cands = set(PHONE_RE.findall(text))
    return sorted({re.sub(r"\s+", " ", c).strip() for c in cands if len(c) >= 7})

def keyword_hit(text: str, keywords: Iterable[str]) -> Set[str]:
    text_l = text.lower()
    return {kw for kw in keywords if kw.lower() in text_l}

def scan_site(base_url: str, keywords: Iterable[str], max_pages: int = 5) -> Dict:
    html = fetch(base_url)
    if not html:
        return {}

    text = extract_text(html)
    hits = keyword_hit(text, keywords)

    if not hits:
        return {}

    emails = find_emails(text)
    phones = find_phones(text)

    return {
        "company": "",
        "website": base_url,
        "contact_name": "",
        "email": ",".join(emails[:3]),
        "phone": ",".join(phones[:3]),
        "source": "website-scan",
        "note": f"Keyword-Hits: {', '.join(sorted(hits))}"
    }

def run(keywords_json: str, targets_path: str = "targets.txt") -> List[Dict]:
    try:
        keywords = json.loads(keywords_json) if keywords_json else []
    except Exception:
        keywords = []

    targets = load_targets(targets_path)
    leads: List[Dict] = []
    for url in targets:
        lead = scan_site(url, keywords)
        if lead:
            leads.append(lead)
        time.sleep(1)
    return leads
