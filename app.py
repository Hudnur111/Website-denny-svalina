import os
from pathlib import Path

from flask import Flask, render_template, request


app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/kontakt")
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if name and email and message:
        inbox = Path("messages.txt")
        inbox.write_text(
            inbox.read_text(encoding="utf-8") + f"\nName: {name}\nE-Mail: {email}\nNachricht: {message}\n---\n"
            if inbox.exists()
            else f"Name: {name}\nE-Mail: {email}\nNachricht: {message}\n---\n",
            encoding="utf-8",
        )

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
