#!/usr/bin/env python3
"""
Lädt die Waldbrandgefahrenindex-Seite des DWD,
extrahiert die Saarland-Stationen und speichert sie als JSON.
"""

import json
import os
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

DWD_URL = "https://www.wettergefahren.de/warnungen/indizes/waldbrand.html"
OUTPUT  = os.path.join(os.path.dirname(__file__), "..", "data", "waldbrand.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; WaldbrandBot/1.0; "
        "+https://github.com/YOUR_GITHUB_NAME/waldbrand-saarland)"
    )
}


def fetch():
    resp = requests.get(DWD_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # Zeitstempel aus Fußzeile
    timestamp_raw = ""
    for tag in soup.find_all(string=re.compile(r"erstellt")):
        m = re.search(r"erstellt\s+([\d.]+\s+[\d:]+)\s+UTC", tag)
        if m:
            timestamp_raw = m.group(1) + " UTC"
            break

    # Saarland-Tabelle finden
    saar_h3 = None
    for h3 in soup.find_all("h3"):
        if "Saarland" in h3.get_text():
            saar_h3 = h3
            break

    if not saar_h3:
        raise ValueError("Saarland-Abschnitt nicht gefunden!")

    # Nächste Tabelle nach der Überschrift
    table = saar_h3.find_next("table")
    rows = table.find_all("tr")

    days = []
    stations = []

    for i, row in enumerate(rows):
        cells = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
        if not cells:
            continue

        if i == 0:
            # Header-Zeile: Stationsname | Do 30.07. | Fr 31.07. | …
            days = [c.split()[0] for c in cells[1:] if c]
            continue

        name = cells[0]
        if not name or name == "Stationsname":
            continue

        values = []
        for v in cells[1:]:
            try:
                values.append(int(v))
            except ValueError:
                values.append(0)

        if values:
            stations.append({"name": name, "days": days, "values": values})

    return {
        "timestamp": timestamp_raw or datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC"),
        "stations": stations,
    }


def main():
    print("Fetching DWD data …")
    html = fetch()
    data = parse(html)
    print(f"  {len(data['stations'])} Saarland-Stationen gefunden.")
    print(f"  Zeitstempel: {data['timestamp']}")

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  JSON gespeichert: {OUTPUT}")


if __name__ == "__main__":
    main()
