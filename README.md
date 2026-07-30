# 🔥 Waldbrandgefahr Saarland

Interaktive Karte der aktuellen Waldbrandgefahr im Saarland – nach dem Vorbild der SWR-Karte für Rheinland-Pfalz.

**Live:** `https://YOUR_GITHUB_NAME.github.io/waldbrand-saarland/`

---

## Features

- 🗺️ **Graue OpenStreetMap** (CartoDB Light)
- 🔴 **Farbige Kreise** nach WBI-Stufe 1–5
- 💬 **SWR-style Tooltip** mit 5-Tage-Prognose
- 🏷️ **Legende** in den WBI-Farbtönen
- 🤖 **Automatische Aktualisierung** 2× täglich via GitHub Actions (6:30 + 12:30 UTC)

## Datenquelle

[Deutscher Wetterdienst – Waldbrand-Gefahrenindex](https://www.wettergefahren.de/warnungen/indizes/waldbrand.html)

Die Daten werden täglich um ca. 6 Uhr UTC vom DWD aktualisiert.

## Struktur

```
waldbrand-saarland/
├── index.html                  ← Karte (GitHub Pages root)
├── data/
│   └── waldbrand.json          ← täglich aktualisierte Daten
├── scripts/
│   └── fetch_waldbrand.py      ← Python-Scraper
└── .github/
    └── workflows/
        └── update.yml          ← GitHub Actions (2× täglich)
```

## Einrichten

### 1. Repository erstellen

```bash
git clone https://github.com/YOUR_GITHUB_NAME/waldbrand-saarland.git
cd waldbrand-saarland
```

### 2. GitHub Pages aktivieren

Im Repository → **Settings → Pages → Source: Deploy from branch (main / root)**

### 3. GitHub Actions aktivieren

Die Datei `.github/workflows/update.yml` aktiviert die automatische Aktualisierung.  
Stelle sicher, dass unter **Settings → Actions → Workflow permissions** "Read and write permissions" aktiviert ist.

### 4. Ersten Datenabruf manuell starten

Im Repository → **Actions → "Waldbrand-Daten aktualisieren" → Run workflow**

---

## WBI-Stufen

| Stufe | Bedeutung        | Farbe   |
|-------|-----------------|---------|
| 1     | Sehr geringe Gefahr | 🟡 gelb |
| 2     | Geringe Gefahr   | 🟠 orange |
| 3     | Mittlere Gefahr  | 🟠 dunkelorange |
| 4     | Hohe Gefahr      | 🔴 rot |
| 5     | Sehr hohe Gefahr | 🔴 dunkelrot |

---

*Datenstand wird automatisch in der Fußzeile der Karte angezeigt.*  
*Quelle: Deutscher Wetterdienst (DWD). Karte: © OpenStreetMap contributors, © CARTO.*
