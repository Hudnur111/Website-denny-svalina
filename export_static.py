from pathlib import Path

from app import app

REPO_BASE = "/Website-denny-svalina"

PAGES = [
    ("/", "index.html"),
    ("/projekte", "projekte/index.html"),
    ("/skills", "skills/index.html"),
    ("/showcase-lab", "showcase-lab/index.html"),
    ("/chatbot", "chatbot/index.html"),
    ("/kontakt", "kontakt/index.html"),
]


def adapt_for_github_pages(html: str) -> str:
    replacements = {
        'href="/': f'href="{REPO_BASE}/',
        'action="/': f'action="{REPO_BASE}/',
        'src="/': f'src="{REPO_BASE}/',
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    html = html.replace('method="POST"', 'method="GET"')
    html = html.replace("Serverseitige Antwortlogik", "Serverseitige Antwortlogik (Live in Flask)")
    html = html.replace(
        "Diese Seite zeigt kleine Funktionen, die komplett serverseitig mit Python berechnet werden.",
        "Diese Seite zeigt die Oberfläche der Python-Demos. Die Berechnung läuft in der Flask-Version.",
    )
    return html


def main() -> None:
    client = app.test_client()

    for route, output_path in PAGES:
        response = client.get(route)
        if response.status_code != 200:
            raise RuntimeError(f"Export failed for {route}: HTTP {response.status_code}")

        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(adapt_for_github_pages(response.data.decode("utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
