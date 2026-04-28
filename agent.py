"""
Automation Execution Agent - Windows Lokale Agent
Draai dit script op je Windows PC.
Het maakt screenshots en voert instructies uit van de Replit server.

INSTALLATIE:
  pip install pyautogui pillow requests pytesseract pygetwindow
  (optioneel voor betere tekst-herkenning: installeer Tesseract OCR)
  https://github.com/UB-Mannheim/tesseract/wiki

GEBRUIK:
  1. Pas REPLIT_URL aan naar jouw Replit app URL
  2. python agent.py
"""

import time
import base64
import json
import sys
import io
import subprocess
from pathlib import Path

# ============================================================
# CONFIGURATIE - Pas dit aan!
# ============================================================
REPLIT_URL = "https://jouw-app.replit.app"   # <-- Vervang dit!
SCREENSHOT_INTERVAL = 2.0  # seconden tussen screenshots
# ============================================================

try:
    import pyautogui
    import requests
    from PIL import Image
    print("✅ Basis modules geladen")
except ImportError as e:
    print(f"❌ Ontbrekende module: {e}")
    print("Voer uit: pip install pyautogui pillow requests")
    sys.exit(1)

# Optioneel: pytesseract voor OCR (tekst herkenning op scherm)
try:
    import pytesseract
    HAS_OCR = True
    print("✅ OCR module geladen (pytesseract)")
except ImportError:
    HAS_OCR = False
    print("⚠️  pytesseract niet gevonden - tekstzoeken minder nauwkeurig")

# Configureer pyautogui
pyautogui.FAILSAFE = True  # Beweeg muis naar hoek om te stoppen
pyautogui.PAUSE = 0.5       # Kleine pauze tussen acties


def maak_screenshot() -> str:
    """Maak een screenshot en retourneer als base64 string."""
    screenshot = pyautogui.screenshot()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def stuur_screenshot(screenshot_b64: str) -> dict:
    """Stuur screenshot naar Replit server, ontvang instructie."""
    try:
        response = requests.post(
            f"{REPLIT_URL}/screenshot",
            json={"screenshot": screenshot_b64},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"❌ Kan niet verbinden met {REPLIT_URL}")
        return {"actie": "wacht", "bericht": "Geen verbinding"}
    except Exception as e:
        print(f"❌ Fout bij versturen screenshot: {e}")
        return {"actie": "wacht"}


def vind_tekst_op_scherm(zoekterm: str) -> tuple:
    """
    Zoek tekst op het scherm via OCR.
    Retourneert (x, y) coordinaten van het gevonden element, of None.
    """
    if not HAS_OCR:
        return None

    try:
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT, lang='nld+eng')

        zoekterm_lower = zoekterm.lower()
        for i, text in enumerate(data['text']):
            if zoekterm_lower in text.lower() and data['conf'][i] > 30:
                x = data['left'][i] + data['width'][i] // 2
                y = data['top'][i] + data['height'][i] // 2
                print(f"  ✅ Tekst gevonden '{text}' op ({x}, {y})")
                return (x, y)

        return None
    except Exception as e:
        print(f"  ⚠️  OCR fout: {e}")
        return None


def vind_en_klik(doel: str) -> bool:
    """
    Zoek een element op het scherm bij naam/tekst en klik erop.
    Gebruikt OCR als beschikbaar, anders pyautogui locateOnScreen.
    """
    print(f"  🔍 Zoeken naar: {doel}")

    # Methode 1: OCR tekst herkenning
    if HAS_OCR:
        coords = vind_tekst_op_scherm(doel)
        if coords:
            x, y = coords
            print(f"  🖱️  Klikken op ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(0.5)
            return True

    # Methode 2: Probeer met pyautogui hotkey als het een knop naam is
    # (fallback - vraag AI om meer context)
    print(f"  ⚠️  Kon '{doel}' niet vinden op scherm")
    return False


def vind_en_typ(doel: str, tekst: str) -> bool:
    """
    Zoek een invoerveld bij label/naam en typ tekst erin.
    """
    print(f"  🔍 Zoeken naar invoerveld: {doel}")
    print(f"  ⌨️  Tekst om in te typen: {tekst}")

    # Zoek het label/veld
    coords = None
    if HAS_OCR:
        coords = vind_tekst_op_scherm(doel)

    if coords:
        x, y = coords
        # Klik iets rechts van het label (waar het invoerveld waarschijnlijk staat)
        pyautogui.click(x + 150, y)
        time.sleep(0.3)
        # Selecteer alles en typ
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(tekst, interval=0.05)
        return True
    else:
        # Probeer te klikken op het actieve veld en typen
        print(f"  ⚠️  Veld niet gevonden, probeer direct typen...")
        pyautogui.typewrite(tekst, interval=0.05)
        return True  # Optimistisch - vraag AI om te verifiëren


def druk_toets(toets: str) -> bool:
    """Druk een toets in."""
    toets_map = {
        "enter": "enter",
        "tab": "tab",
        "escape": "esc",
        "esc": "esc",
        "delete": "delete",
        "backspace": "backspace",
        "space": "space",
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4",
        "f5": "f5", "f6": "f6", "f7": "f7", "f8": "f8",
    }
    toets_naam = toets_map.get(toets.lower(), toets.lower())
    print(f"  ⌨️  Toets indrukken: {toets_naam}")
    pyautogui.press(toets_naam)
    time.sleep(0.3)
    return True


def voer_instructie_uit(instructie: dict) -> bool:
    """
    Voer een instructie uit van de Replit server.
    Retourneert True als succesvol, False als mislukt.
    """
    actie = instructie.get("actie", "")
    doel = instructie.get("doel", "")
    tekst = instructie.get("tekst", "")
    toets = instructie.get("toets", "")

    print(f"\n📋 Instructie: {actie}")
    if doel: print(f"   Doel: {doel}")
    if tekst: print(f"   Tekst: {tekst}")
    if instructie.get("redenering"): print(f"   Redenering: {instructie['redenering']}")

    if actie == "wacht":
        print("  ⏳ Wachten...")
        return True

    elif actie == "find_and_click":
        return vind_en_klik(doel)

    elif actie == "find_and_type":
        return vind_en_typ(doel, tekst)

    elif actie == "press_key":
        return druk_toets(toets)

    elif actie == "type":
        print(f"  ⌨️  Typen: {tekst}")
        pyautogui.typewrite(tekst, interval=0.05)
        return True

    elif actie == "click":
        return vind_en_klik(doel)

    elif actie == "vraag":
        print(f"\n❓ AI vraag: {instructie.get('vraag')}")
        print("  (Antwoord via de Replit web interface)")
        return True

    elif actie == "klaar":
        print("  ✅ Rij voltooid!")
        return True

    else:
        print(f"  ⚠️  Onbekende actie: {actie}")
        return False


def controleer_verbinding() -> bool:
    """Test de verbinding met de Replit server."""
    try:
        response = requests.get(f"{REPLIT_URL}/status", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Verbonden met Replit server (status: {data.get('status', 'onbekend')})")
        return True
    except Exception as e:
        print(f"❌ Kan niet verbinden met {REPLIT_URL}: {e}")
        return False


def main():
    """Hoofdlus van de agent."""
    print("=" * 60)
    print("  Automation Execution Agent - Windows Client")
    print("=" * 60)
    print(f"  Server: {REPLIT_URL}")
    print(f"  Screenshot interval: {SCREENSHOT_INTERVAL}s")
    print(f"  OCR beschikbaar: {'Ja' if HAS_OCR else 'Nee'}")
    print("=" * 60)
    print("\nTip: Beweeg muis naar hoek van scherm om te stoppen (PyAutoGUI failsafe)\n")

    # Test verbinding
    if not controleer_verbinding():
        print("\nPas REPLIT_URL aan in dit script en probeer opnieuw.")
        sys.exit(1)

    print("\n🚀 Agent gestart! Klaar om taken uit te voeren.")
    print("   Ga naar de Replit web interface om te starten.\n")

    laatste_actie = None

    while True:
        try:
            # Maak screenshot
            print("📸 Screenshot maken...", end=" ", flush=True)
            screenshot_b64 = maak_screenshot()
            print("klaar")

            # Stuur naar server en ontvang instructie
            instructie = stuur_screenshot(screenshot_b64)

            actie = instructie.get("actie", "wacht")

            # Klaar melding
            if actie == "klaar" and instructie.get("bericht") == "Alle rijen verwerkt!":
                print("\n🎉 Alle rijen verwerkt! Taak voltooid.")
                break

            # Voer instructie uit
            if actie != "wacht" or laatste_actie != "wacht":
                succes = voer_instructie_uit(instructie)
                if not succes:
                    print("  ⚠️  Instructie niet succesvol uitgevoerd")

            laatste_actie = actie

            # Wacht voor volgende iteratie
            time.sleep(SCREENSHOT_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n⛔ Agent gestopt door gebruiker.")
            break
        except Exception as e:
            print(f"\n❌ Onverwachte fout: {e}")
            print("   Opnieuw proberen in 5 seconden...")
            time.sleep(5)


if __name__ == "__main__":
    main()
