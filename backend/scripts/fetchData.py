import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

CSV_PATH = "data/SB_publication_PMC.csv"
OUT_DIR = "data/fetched_texts"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
}

for i, row in df.iterrows():
    url = row.get("Link") or row.get("URL") or row.get("link")
    if not url or not isinstance(url, str):
        continue

    out_file = os.path.join(OUT_DIR, f"{i}.txt")
    if os.path.exists(out_file):
        continue

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        text = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
        if text:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
        time.sleep(1)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
