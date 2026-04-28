"""
Automation Execution Agent - Flask Server (Replit)
Ontvangt screenshots van de Windows agent, analyseert ze met AI,
en stuurt instructies terug om de taak uit te voeren.
"""

import os
import json
import base64
import threading
from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import openpyxl
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "automation-agent-secret")

# OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Globale staat (in productie: gebruik een database)
state = {
    "rows": [],           # Excel rijen: [{referentie, waarde}, ...]
    "current_index": 0,   # Huidige rij in verwerking
    "status": "idle",     # idle / running / paused / done
    "log": [],            # Workflow log
    "last_screenshot": None,  # Base64 van laatste screenshot
    "pending_question": None, # Vraag voor de gebruiker
    "user_answer": None,      # Antwoord van de gebruiker
    "workflow": [],           # Geleerde stappen
    "phase": 1,               # Leerfase 1-5
}
state_lock = threading.Lock()


def log(message, level="info"):
    """Voeg een bericht toe aan de log."""
    entry = {"level": level, "message": message}
    with state_lock:
        state["log"].append(entry)
    print(f"[{level.upper()}] {message}")


def analyse_screenshot(screenshot_b64, referentie, waarde, context=""):
    """
    Stuur screenshot naar GPT-4o Vision en vraag wat te doen.
    Retourneert een instructie-dict.
    """
    prompt = f"""Je bent een automatiseringsagent die een computerscherm bekijkt.

Huidige taak:
- Zoek het zoekveld op het scherm
- Typ deze referentie in: "{referentie}"
- Na het zoeken: zoek het veld waar de waarde moet komen
- Vul deze waarde in: "{waarde}"

Extra context: {context if context else "geen"}

Analyseer het scherm en geef EEN instructie terug als JSON:
{{
  "actie": "find_and_type" | "find_and_click" | "press_key" | "wait" | "vraag" | "klaar",
  "doel": "beschrijving van wat je zoekt (bv: 'zoekveld met label Referentie')",
  "tekst": "tekst om in te typen (alleen bij find_and_type)",
  "toets": "toetsnaam (alleen bij press_key, bv: Enter, Tab)",
  "vraag": "jouw vraag aan de gebruiker (alleen bij actie=vraag)",
  "redenering": "waarom je deze actie kiest"
}}

Regels:
- Gebruik NOOIT pixel-coördinaten
- Beschrijf elementen bij hun zichtbare tekst, label of positie
- Als je het zoekveld al hebt ingevuld en het zoekresultaat ziet, zoek dan het tweede veld
- Als je iets niet zeker weet, gebruik actie "vraag"
- Als de taak volledig klaar is, gebruik actie "klaar"
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_b64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
        response_format={"type": "json_object"}
    )

    try:
        instructie = json.loads(response.choices[0].message.content)
        return instructie
    except Exception as e:
        log(f"Fout bij parsen AI antwoord: {e}", "error")
        return {"actie": "vraag", "vraag": "Ik kon het scherm niet goed analyseren. Kan je meer context geven?"}


@app.route("/")
def index():
    """Hoofdpagina."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_excel():
    """Ontvang en parseer Excel bestand."""
    if "file" not in request.files:
        return jsonify({"error": "Geen bestand gevonden"}), 400

    file = request.files["file"]
    if not file.filename.endswith((".xlsx", ".xls")):
        return jsonify({"error": "Alleen Excel bestanden (.xlsx, .xls) toegestaan"}), 400

    try:
        wb = openpyxl.load_workbook(BytesIO(file.read()))
        ws = wb.active

        rows = []
        for row in ws.iter_rows(min_row=2, values_only=True):  # Sla header over
            if row[0] is not None:
                rows.append({
                    "referentie": str(row[0]),
                    "waarde": str(row[1]) if row[1] is not None else "",
                    "status": "wachtend"
                })

        with state_lock:
            state["rows"] = rows
            state["current_index"] = 0
            state["status"] = "idle"
            state["log"] = []

        log(f"{len(rows)} rijen geladen uit Excel")
        return jsonify({"success": True, "rijen": len(rows), "preview": rows[:5]})

    except Exception as e:
        log(f"Fout bij inlezen Excel: {e}", "error")
        return jsonify({"error": str(e)}), 500


@app.route("/screenshot", methods=["POST"])
def ontvang_screenshot():
    """
    Ontvang screenshot van Windows agent.
    Analyseer met AI en stuur instructie terug.
    """
    with state_lock:
        if state["status"] != "running":
            return jsonify({"actie": "wacht", "bericht": f"Status: {state['status']}"})

        if state["current_index"] >= len(state["rows"]):
            state["status"] = "done"
            return jsonify({"actie": "klaar", "bericht": "Alle rijen verwerkt!"})

        # Wacht op gebruikersantwoord als er een vraag open staat
        if state["pending_question"] and not state["user_answer"]:
            return jsonify({"actie": "wacht", "bericht": "Wacht op antwoord gebruiker..."})

    data = request.get_json()
    if not data or "screenshot" not in data:
        return jsonify({"error": "Geen screenshot ontvangen"}), 400

    screenshot_b64 = data["screenshot"]

    with state_lock:
        state["last_screenshot"] = screenshot_b64
        huidig = state["rows"][state["current_index"]]
        referentie = huidig["referentie"]
        waarde = huidig["waarde"]
        context = state["user_answer"] or ""
        state["user_answer"] = None  # Reset antwoord

    log(f"Screenshot ontvangen voor rij {state['current_index'] + 1}: referentie={referentie}")

    # AI analyse
    instructie = analyse_screenshot(screenshot_b64, referentie, waarde, context)

    # Log de stap
    log(f"AI instructie: {instructie.get('actie')} - {instructie.get('redenering', '')}")

    # Sla workflow stap op
    with state_lock:
        state["workflow"].append({
            "rij": state["current_index"] + 1,
            "referentie": referentie,
            "instructie": instructie
        })

        # Behandel speciale acties
        if instructie.get("actie") == "vraag":
            state["pending_question"] = instructie.get("vraag")
            log(f"AI vraagt: {instructie.get('vraag')}", "warning")

        elif instructie.get("actie") == "klaar":
            state["rows"][state["current_index"]]["status"] = "klaar"
            state["current_index"] += 1
            state["pending_question"] = None
            log(f"Rij {state['current_index']} voltooid!", "success")

            if state["current_index"] >= len(state["rows"]):
                state["status"] = "done"
                log("Alle rijen verwerkt! Taak voltooid.", "success")

    return jsonify(instructie)


@app.route("/status", methods=["GET"])
def get_status():
    """Geef huidige voortgang terug."""
    with state_lock:
        return jsonify({
            "status": state["status"],
            "totaal": len(state["rows"]),
            "huidig": state["current_index"],
            "rijen": state["rows"],
            "log": state["log"][-20:],  # Laatste 20 logs
            "pending_question": state["pending_question"],
            "heeft_screenshot": state["last_screenshot"] is not None,
            "fase": state["phase"]
        })


@app.route("/screenshot/latest", methods=["GET"])
def get_latest_screenshot():
    """Geef het laatste screenshot terug voor de UI."""
    with state_lock:
        if state["last_screenshot"]:
            return jsonify({"screenshot": state["last_screenshot"]})
        return jsonify({"screenshot": None})


@app.route("/control", methods=["POST"])
def control():
    """Start, pauzeer of stop de automatisering."""
    data = request.get_json()
    actie = data.get("actie")

    with state_lock:
        if actie == "start":
            if len(state["rows"]) == 0:
                return jsonify({"error": "Geen Excel geladen"}), 400
            state["status"] = "running"
            state["current_index"] = 0
            for rij in state["rows"]:
                rij["status"] = "wachtend"
            log("Automatisering gestart!")
        elif actie == "pause":
            state["status"] = "paused"
            log("Automatisering gepauzeerd.")
        elif actie == "stop":
            state["status"] = "idle"
            state["current_index"] = 0
            log("Automatisering gestopt.")
        elif actie == "resume":
            state["status"] = "running"
            log("Automatisering hervat.")

    return jsonify({"success": True, "status": state["status"]})


@app.route("/feedback", methods=["POST"])
def feedback():
    """Ontvang antwoord van gebruiker op AI vraag."""
    data = request.get_json()
    antwoord = data.get("antwoord", "")

    with state_lock:
        state["user_answer"] = antwoord
        state["pending_question"] = None
        log(f"Gebruiker antwoordde: {antwoord}")

    return jsonify({"success": True})


@app.route("/workflow", methods=["GET"])
def get_workflow():
    """Geef de geleerde workflow terug."""
    with state_lock:
        return jsonify({"workflow": state["workflow"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
