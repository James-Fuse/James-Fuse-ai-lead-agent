import re
import time
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Iterable, Set

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; James-Fuse-LeadAgent/1.0)"}

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
    return {kw for k
