import re
from email.utils import parseaddr

from flask import Flask, render_template, request

app = Flask(__name__)

PROJECTS = [
    {
        "title": "Serverseitige Suchfunktion",
        "category": "Backend",
        "description": "Eine Suchseite, die Titel, Kategorien, Beschreibung und Tags komplett in Python filtert.",
        "tags": ["Python", "Flask", "Suche"],
        "result": "Zeigt, wie Benutzereingaben sauber gelesen, normalisiert und verarbeitet werden.",
    },
    {
        "title": "Kontaktformular mit Validierung",
        "category": "Formulare",
        "description": "Ein Formular mit Pflichtfeldern, E-Mail-Prüfung und klarer Rückmeldung nach dem Absenden.",
        "tags": ["HTML", "POST", "Validierung"],
        "result": "Macht sichtbar, dass Frontend-Struktur und Backend-Logik zusammenspielen.",
    },
    {
        "title": "Mini-Chatbot ohne JavaScript",
        "category": "Backend",
        "description": "Ein regelbasierter Assistent, der Antworten serverseitig über Flask erzeugt.",
        "tags": ["Python", "Logik", "Chatbot"],
        "result": "Demonstriert einfache Textanalyse, Bedingungen und wiederverwendbare Funktionen.",
    },
    {
        "title": "Mehrseitige Webstruktur",
        "category": "Frontend",
        "description": "Gemeinsames Basis-Template, klare Navigation und ein einheitliches Layout für alle Seiten.",
        "tags": ["HTML", "CSS", "Templates"],
        "result": "Wirkt wie ein kleines echtes Webprojekt statt wie eine einzelne Übungsseite.",
    },
]

SKILLS = [
    {
        "name": "HTML",
        "level": 88,
        "text": "Semantische Seitenstruktur, Navigation, Formulare, Listen und klare Inhaltsbereiche.",
    },
    {
        "name": "CSS",
        "level": 84,
        "text": "Responsive Layouts, moderne Karten, saubere Abstände, Zustände und visuelle Hierarchie.",
    },
    {
        "name": "Python",
        "level": 78,
        "text": "Funktionen, Listen, Dictionaries, Bedingungen und Verarbeitung von Benutzereingaben.",
    },
    {
        "name": "Flask",
        "level": 70,
        "text": "Routing, Templates, GET/POST-Formulare, Validierung und serverseitige Antworten.",
    },
]

METRICS = [
    {"value": "5", "label": "Seiten"},
    {"value": "4", "label": "Python-Routen"},
    {"value": "0", "label": "JavaScript-Dateien"},
    {"value": "100%", "label": "Serverseitige Logik"},
]

FAQ_ANSWERS = {
    "python": "Python wird hier für Routing, Suche, Formularprüfung und die Chatbot-Logik eingesetzt.",
    "flask": "Flask verbindet die HTML-Templates mit Python-Funktionen und verarbeitet die Formularanfragen.",
    "html": "HTML sorgt für die semantische Struktur: Navigation, Inhalte, Projektkarten und Formulare.",
    "css": "CSS gestaltet Layout, Farben, Abstände, Fokuszustände und die responsive Darstellung.",
    "bewerbung": "Das Projekt zeigt technische Grundlagen kompakt und professionell, ohne private Daten offenzulegen.",
    "kontakt": "Das Kontaktformular prüft Pflichtfelder und E-Mail-Adresse serverseitig mit Python.",
}


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\wäöüÄÖÜß-]+\b", text))


def analyze_text(text: str) -> dict:
    cleaned = text.strip()
    words = count_words(cleaned)
    sentences = len(re.findall(r"[.!?]+", cleaned)) or (1 if cleaned else 0)
    reading_minutes = max(1, round(words / 180)) if words else 0

    if not cleaned:
        quality = "Warte auf Eingabe"
        tip = "Füge einen Text ein, um Wortzahl, Satzanzahl und Lesedauer zu berechnen."
    elif words < 20:
        quality = "Kurz und direkt"
        tip = "Für ein Anschreiben darf der Text etwas konkreter werden: Motivation, Stärke und Beispiel nennen."
    elif words <= 90:
        quality = "Gut scanbar"
        tip = "Die Länge ist angenehm. Achte darauf, dass der wichtigste Punkt direkt am Anfang steht."
    else:
        quality = "Ausführlich"
        tip = "Kürze lange Sätze und bringe die stärkste Aussage in die ersten zwei Zeilen."

    return {
        "characters": len(cleaned),
        "words": words,
        "sentences": sentences,
        "reading_minutes": reading_minutes,
        "quality": quality,
        "tip": tip,
    }


def calculate_project_score(form: dict) -> dict:
    checked_items = [
        form.get("responsive") == "on",
        form.get("validation") == "on",
        form.get("search") == "on",
        form.get("clean_design") == "on",
        form.get("documentation") == "on",
    ]
    score = sum(checked_items) * 20

    if score >= 80:
        label = "Starkes Bewerbungsprojekt"
        text = "Das Projekt zeigt mehrere wichtige Grundlagen und wirkt gut präsentierbar."
    elif score >= 50:
        label = "Solide Basis"
        text = "Die Richtung stimmt. Mit mehr Interaktion oder besserer Dokumentation wird es stärker."
    else:
        label = "Ausbaufähig"
        text = "Ein paar sichtbare Funktionen helfen, damit Arbeitgeber den technischen Anteil schneller erkennen."

    return {"score": score, "label": label, "text": text}


def is_valid_email(value: str) -> bool:
    parsed_name, parsed_email = parseaddr(value)
    return not parsed_name and "@" in parsed_email and "." in parsed_email.rsplit("@", 1)[-1]


def chatbot_answer(message: str) -> str:
    cleaned = message.lower().strip()

    if not cleaned:
        return "Bitte gib eine kurze Frage ein."

    if "hallo" in cleaned or "hi" in cleaned or "hey" in cleaned:
        return "Hallo! Frag mich gerne nach Python, Flask, HTML, CSS, Kontakt oder Bewerbung."

    for keyword, answer in FAQ_ANSWERS.items():
        if keyword in cleaned:
            return answer

    return (
        "Dazu habe ich keine feste Antwort. Die Demo zeigt aber, wie ein einfacher "
        "Chatbot serverseitig mit Python funktionieren kann."
    )


@app.route("/")
def index():
    return render_template("index.html", projects=PROJECTS[:3], skills=SKILLS, metrics=METRICS)


@app.route("/projekte")
def projects():
    query = request.args.get("q", "").strip().lower()

    if query:
        filtered_projects = [
            project
            for project in PROJECTS
            if query in project["title"].lower()
            or query in project["category"].lower()
            or query in project["description"].lower()
            or query in project["result"].lower()
            or any(query in tag.lower() for tag in project["tags"])
        ]
    else:
        filtered_projects = PROJECTS

    return render_template("projects.html", projects=filtered_projects, query=query)


@app.route("/skills")
def skills():
    return render_template("skills.html", skills=SKILLS)


@app.route("/showcase-lab", methods=["GET", "POST"])
def showcase_lab():
    text_input = ""
    text_result = analyze_text("")
    score_result = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "text":
            text_input = request.form.get("text_input", "")
            text_result = analyze_text(text_input)

        if action == "score":
            score_result = calculate_project_score(request.form)

    return render_template(
        "showcase_lab.html",
        text_input=text_input,
        text_result=text_result,
        score_result=score_result,
    )


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    user_message = ""
    bot_answer = "Stelle eine Frage zu HTML, CSS, Python, Flask, Kontakt oder Bewerbung."

    if request.method == "POST":
        user_message = request.form.get("message", "")
        bot_answer = chatbot_answer(user_message)

    return render_template("chatbot.html", user_message=user_message, bot_answer=bot_answer)


@app.route("/kontakt", methods=["GET", "POST"])
def contact():
    result = None
    form_data = {"name": "", "email": "", "topic": "", "message": ""}

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "topic": request.form.get("topic", "").strip(),
            "message": request.form.get("message", "").strip(),
        }

        if not form_data["name"] or not form_data["email"] or not form_data["message"]:
            result = {
                "type": "error",
                "text": "Bitte fülle Name, E-Mail und Nachricht aus.",
            }
        elif not is_valid_email(form_data["email"]):
            result = {
                "type": "error",
                "text": "Bitte gib eine gültige E-Mail-Adresse ein.",
            }
        else:
            topic = form_data["topic"] or "Allgemein"
            result = {
                "type": "success",
                "text": f"Vielen Dank, {form_data['name']}. Deine Nachricht zum Thema '{topic}' wurde serverseitig verarbeitet.",
            }
            form_data = {"name": "", "email": "", "topic": "", "message": ""}

    return render_template("contact.html", result=result, form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
