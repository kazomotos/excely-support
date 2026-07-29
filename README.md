# Excely Website

Statische Marketing-, Support- und Datenschutzwebsite für Excely auf macOS und
iOS. Die Seite richtet sich an Teams und Unternehmen, die wiederkehrende
Eingaben in Excel-Arbeitsmappen strukturieren möchten.

## Inhalt

- `index.html`: Produktseite mit Vorteilen, Funktionsweise, Voraussetzungen
  und Kontaktmöglichkeit
- `datenschutz.html`: gemeinsame Datenschutzerklärung für Website und App
- `styles.css`: responsives Layout ohne externe Schriftarten, Skripte oder
  Tracking
- `assets/screenshots`: weboptimierte, echte Screenshots der Excely-App
- `assets/excely-mark.png`: gemeinsames Markenzeichen der Website und Apps
- `scripts/validate-site.py`: lokale Struktur-, Link- und Datenschutzprüfung

## Lokal prüfen

```sh
python3 scripts/validate-site.py
python3 -m http.server 8000
```

Danach sind die Seiten unter `http://localhost:8000/` und
`http://localhost:8000/datenschutz.html` erreichbar.

## GitHub Pages veröffentlichen

1. Repository **Settings** öffnen.
2. Unter **Pages** bei *Build and deployment* **Deploy from a branch** wählen.
3. Branch `main` und Ordner `/(root)` auswählen und speichern.
4. Nach dem Deployment lauten die URLs:
   - Marketing und Support: `https://kazomotos.github.io/excely-support/`
   - Datenschutz: `https://kazomotos.github.io/excely-support/datenschutz.html`

Die Datenschutzerklärung beschreibt die derzeit dokumentierten Funktionen und
Dienste. Änderungen an Hosting, Analyse, App-Funktionen oder Datenflüssen müssen
vor Veröffentlichung auch dort nachvollzogen und rechtlich geprüft werden.
