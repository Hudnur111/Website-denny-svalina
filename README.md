# Denny Portfolio Website

Moderne persoenliche Website fuer GitHub Pages. Die Seite besteht aus statischem HTML und CSS und kann direkt aus dem Repository veroeffentlicht werden.

## Dateien

- `index.html` enthaelt die komplette Seitenstruktur.
- `style.css` enthaelt Design, Responsive Layouts und CSS-Animationen.
- `app.py` ist optional fuer lokales Testen mit Flask. GitHub Pages fuehrt Python-Dateien nicht aus.

## Lokal ansehen

Oeffne `index.html` direkt im Browser oder starte optional Flask:

```bash
pip install flask
python app.py
```

Danach ist die lokale Version unter `http://127.0.0.1:5000/` erreichbar.

## Auf GitHub Pages veroeffentlichen

1. Erstelle ein neues GitHub-Repository.
2. Lade `index.html`, `style.css`, `README.md`, `.gitignore` und optional `app.py` hoch.
3. Gehe im Repository zu `Settings` > `Pages`.
4. Waehle bei `Build and deployment` die Quelle `Deploy from a branch`.
5. Waehle den Branch `main` und den Ordner `/root`.
6. Speichere die Einstellung und warte kurz, bis GitHub die Pages-URL erstellt.

## Kontaktformular

GitHub Pages ist statisch und kann kein Python-Backend ausfuehren. Das Formular nutzt deshalb `mailto:` und oeffnet das Mailprogramm mit einer vorbereiteten Nachricht an `denny.svalin2@gmail.com`.
