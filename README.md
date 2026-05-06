# Bewerbungs-Showcase

Eine mehrseitige Bewerbungswebsite mit HTML, CSS und Python Flask.

Das Projekt zeigt eine saubere Webstruktur, serverseitige Verarbeitung und ein modernes responsives Design. Es verwendet bewusst kein JavaScript.

## Funktionen

- Startseite mit professioneller Projektpräsentation
- Projektübersicht mit serverseitiger Suche
- Skill-Seite mit CSS-Fortschrittsbalken
- Showcase-Lab mit Textanalyse und Projekt-Score
- Kontaktformular mit Python-Validierung
- Mini-Chatbot mit regelbasierter Flask-Logik
- Wiederverwendbares Basis-Template
- Responsive Design für Desktop und Smartphone

## Installation

```bash
pip install -r requirements.txt
python app.py
```

Danach im Browser öffnen:

```text
http://127.0.0.1:5000
```

## Deployment

Dieses Projekt ist eine Flask-App. Für eine Live-Version mit Python-Backend eignet sich Render, Railway oder PythonAnywhere. GitHub Pages kann nur statische HTML/CSS/JS-Seiten ausführen.

Für Render sind `Procfile`, `render.yaml` und `gunicorn` bereits vorbereitet.

## Struktur

```text
bewerbungs_showcase_html_css_python/
|-- app.py
|-- requirements.txt
|-- README.md
|-- Procfile
|-- render.yaml
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- projects.html
|   |-- skills.html
|   |-- showcase_lab.html
|   |-- chatbot.html
|   `-- contact.html
`-- static/
    `-- css/
        `-- style.css
```
