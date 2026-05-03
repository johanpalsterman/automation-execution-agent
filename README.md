# 🤖 Automation Execution Agent

> Een AI-gestuurde automatiseringstool die repetitieve taken uitvoert door je scherm te bekijken en contextueel te handelen — zoals een mens, maar dan 24/7.

---

## 📱 Apparaat Ondersteuning

| Apparaat | Rol | Ondersteuning |
|----------|-----|:-------------:|
| Windows PC / Mac | Lokale agent (screenshots + klikken) | ✅ Volledig |
| iPhone / iPad | Web interface (beheer + monitoring) | ✅ Volledig |
| Android | Web interface (beheer + monitoring) | ✅ Volledig |
| Linux | Lokale agent (screenshots + klikken) | ✅ Volledig |

> **Belangrijk:** iPhone en iPad kunnen de web interface volledig bedienen — Excel uploaden, starten, pauzeren, vragen beantwoorden en live meekijken. De lokale agent (die het scherm bestuurt) moet draaien op een Windows PC, Mac of Linux machine.

---

## 🏗️ Hoe het werkt

```
[Excel met referenties]
         ↓
[Replit web app] ←→ [Windows/Mac/Linux agent op jouw PC]
         ↓
[GPT-4o Vision analyseert screenshot]
         ↓
[Instructies: klik hier, typ dit]
         ↓
[Jij bewaakt via iPhone/iPad/browser]
```

1. Je laadt een Excel op via de web interface (ook op iPhone/iPad)
2. De lokale agent stuurt continu screenshots naar de Replit server
3. De AI ziet het scherm, begrijpt de interface en geeft instructies
4. De agent voert de instructies uit (klikken, typen, etc.)
5. Bij twijfel stelt de AI een vraag — jij antwoordt via de web interface (ook op telefoon!)

---

## ⚡ Snelstart

### Stap 1 — Replit opzetten

1. Ga naar [replit.com](https://replit.com) en maak een account aan
2. Klik op **+ Create Repl** → kies **Python**
3. Geef het een naam (bijv. `automation-agent`)
4. Upload de volgende bestanden:
   - `app.py`
   - `requirements.txt`
   - Map `templates/` met daarin `index.html`

### Stap 2 — OpenAI API Key instellen

1. Ga in Replit naar **Secrets** (sleutel-icoontje in de zijbalk)
2. Voeg toe:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** jouw OpenAI API key (van [platform.openai.com](https://platform.openai.com))

### Stap 3 — Replit starten

1. Klik op **Run**
2. De web interface verschijnt
3. Kopieer de URL (bijv. `https://automation-agent.jouw-naam.replit.app`)

> 💡 **iPhone/iPad tip:** Sla deze URL op als bladwijzer of voeg toe aan je beginscherm via Delen → Zet op beginscherm

---

### Stap 4 — Lokale agent installeren (PC/Mac/Linux)

#### Windows
```cmd
pip install pyautogui pillow requests pytesseract pygetwindow
```

#### Mac
```bash
pip3 install pyautogui pillow requests pytesseract pygetwindow
brew install tesseract
```

#### Linux
```bash
pip3 install pyautogui pillow requests pytesseract python-xlib
sudo apt install tesseract-ocr
```

**Agent configureren:**
Open `agent.py` en pas de eerste regel aan:
```python
REPLIT_URL = "https://automation-agent.jouw-naam.replit.app"  # ← jouw URL hier
```

**Agent starten:**
```bash
python agent.py        # Windows
python3 agent.py       # Mac / Linux
```

---

### Stap 5 — Excel voorbereiden

Maak een Excel bestand (`.xlsx`) met minimaal 2 kolommen:

| Referentie    | Waarde          |
|---------------|-----------------|
| REF-001       | BTW-BE123456789 |
| REF-002       | BTW-BE987654321 |
| KLANT-2024-05 | info@bedrijf.be |

- **Rij 1:** Headers (worden automatisch overgeslagen)
- **Kolom A:** De referentie om op te zoeken
- **Kolom B:** De waarde om in te vullen

---

### Stap 6 — Gebruik

1. ✅ Replit app draait
2. ✅ `agent.py` draait op je Windows/Mac/Linux machine
3. ✅ Open de web interface (ook op iPhone/iPad!)
4. Upload je Excel bestand via de knop
5. Klik **▶ Start**
6. De agent gaat automatisch aan de slag!

---

## 📱 iPhone & iPad — Web Interface

De volledige web interface werkt op iPhone en iPad via Safari of Chrome.

### Wat je kunt doen via je telefoon:
- 📂 Excel bestand uploaden (vanuit Bestanden-app, iCloud of e-mail)
- ▶ Start / ⏸ Pauzeer / ⏹ Stop de automatisering
- 🖥️ Live screenshot van de agent bekijken
- 🤔 Vragen van de AI beantwoorden
- 📜 Activiteiten log bekijken
- 📊 Voortgang en statistieken volgen

### Toevoegen aan beginscherm (iPhone/iPad):
1. Open de Replit URL in **Safari**
2. Tik op het **Deel-icoontje** (vierkant met pijl omhoog)
3. Kies **"Zet op beginscherm"**
4. Geef het een naam (bijv. "Automation Agent")
5. De app verschijnt als icoontje op je beginscherm!

### Wat NIET mogelijk is op iPhone/iPad:
- ❌ De lokale agent draaien (iOS staat geen automatische schermbesturing toe)
- ❌ PyAutoGUI of screenshottools installeren

> **De agent moet altijd draaien op een Windows, Mac of Linux machine.** Je iPhone/iPad is de afstandsbediening!

---

## 🖥️ iPhone als afstandsbediening — PC bedienen via je telefoon

Wil je niet alleen de web interface gebruiken, maar ook het **scherm van je PC live zien en bedienen** vanaf je iPhone? Dat kan via een gratis Remote Desktop app.

### Hoe het werkt

```
iPhone (jij kijkt + bedient)
        ↕ Remote Desktop app
PC (agent.py draait + bestuurt scherm)
        ↕ screenshots
Replit server (AI analyseert)
```

Je iPhone wordt het venster én het stuur — de agent draait gewoon op de PC op de achtergrond. Ideaal als je weg bent van je bureau maar de automatisering wilt bewaken of ingrijpen.

---

### 📲 Beste gratis opties

| App | Gratis | Kwaliteit | Moeilijkheid |
|-----|:------:|-----------|:------------:|
| **Chrome Remote Desktop** | ✅ | Goed | Makkelijk |
| **Microsoft Remote Desktop** | ✅ | Zeer goed | Middel |
| **AnyDesk** | ✅ (privé) | Goed | Makkelijk |
| **TeamViewer** | ✅ (privé) | Zeer goed | Makkelijk |

---

### ⚡ Snelstart met Chrome Remote Desktop (aanbevolen)

#### Op je PC:
1. Open **Google Chrome** → ga naar [remotedesktop.google.com](https://remotedesktop.google.com)
2. Klik op **"Externe toegang instellen"**
3. Download en installeer de Chrome Remote Desktop extensie
4. Geef je PC een naam en stel een PIN in (min. 6 cijfers)
5. Start `agent.py` in een Command Prompt venster
6. Laat alles draaien — je PC hoeft alleen aan te blijven

#### Op je iPhone/iPad:
1. Download **Chrome Remote Desktop** uit de App Store (gratis)
2. Log in met **hetzelfde Google-account** als op je PC
3. Tik op de naam van je PC in de lijst
4. Voer de PIN in
5. Je ziet nu het scherm van je PC live op je telefoon!

#### Combinatie met de agent:
- Open de **Replit web interface** in een apart browsertabblad op je iPhone → voor starten/stoppen en AI-vragen beantwoorden
- Gebruik **Chrome Remote Desktop** om het scherm te bewaken → voor ingrijpen als de agent vastloopt
- Je kunt ook via Remote Desktop direct `agent.py` starten of stoppen vanuit de Command Prompt

---

### 💡 Tips

- **Slaapstand voorkomen:** Zorg dat je PC niet in slaapstand gaat tijdens de automatisering
  - Windows: Instellingen → Energiebeheer → Nooit in slaapstand
- **Scherm uitzetten mag wel:** De monitor mag uit, de PC hoeft alleen aan te blijven
- **Thuis netwerk vs. buiten:** Chrome Remote Desktop werkt ook buiten je thuisnetwerk via internet
- **Meerdere schermen:** In Chrome Remote Desktop kun je tussen schermen wisselen via het menu

---

## 🔒 Veiligheid

- **PyAutoGUI Failsafe:** Beweeg je muis snel naar de **linkerbovenhoek** van je scherm om de agent onmiddellijk te stoppen
- De agent kan niet op eigen initiatief starten — altijd via de web interface
- Zet een sterk wachtwoord op je Replit account
- Deel de Replit URL niet met onbekenden

---

## 🛠️ Problemen oplossen

| Probleem | Oplossing |
|----------|-----------|
| Agent kan niet verbinden | Controleer of `REPLIT_URL` correct is in `agent.py` |
| AI vindt veld niet | Beantwoord de AI-vraag via de web interface met meer context |
| Screenshots komen niet aan | Controleer firewall / Windows Defender instellingen |
| Tesseract fout | Zorg dat Tesseract geïnstalleerd en in je PATH staat |
| iPhone: kan geen Excel uploaden | Sla het bestand eerst op in de Bestanden-app of iCloud Drive |
| Replit stopt na inactiviteit | Gratis Replit-accounts slapen na ~30 min; upgrade of gebruik een wake-service |

---

## 📦 Vereisten

### Server (Replit) — `requirements.txt`
```
flask>=3.0.0
openai>=1.0.0
openpyxl>=3.1.0
pillow>=10.0.0
gunicorn>=21.0.0
```

### Lokale agent (jouw PC) — `agent_requirements.txt`
```
pyautogui>=0.9.54
pillow>=10.0.0
requests>=2.31.0
pytesseract>=0.3.10
pygetwindow>=0.0.9
```

---

## 🗺️ Roadmap

- [x] **v1.0** — Basis automatisering: Excel → screenshots → AI instructies
- [x] **v1.0** — Web interface met live screenshot viewer
- [x] **v1.0** — AI vraag-en-antwoord via web interface
- [x] **v1.0** — Volledige iPhone/iPad ondersteuning via web
- [ ] **v1.1** — Workflow opslaan en hergebruiken
- [ ] **v1.2** — AI demonstreert stap voor stap aan gebruiker
- [ ] **v1.3** — Stap-voor-stap goedkeuring modus
- [ ] **v1.4** — Periodieke controle modus (scheduled runs)
- [ ] **v1.5** — Multi-monitor ondersteuning
- [ ] **v2.0** — Volledig autonome modus met rapportage

---

## 📚 Links

- [OpenAI Platform](https://platform.openai.com) — API key aanmaken
- [Replit](https://replit.com) — Server hosting
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) — OCR voor Windows
- [PyAutoGUI docs](https://pyautogui.readthedocs.io) — Automatiseringsbibliotheek

---

## 📋 Release Notes

Zie [RELEASE_NOTES.md](./RELEASE_NOTES.md) voor alle versie-informatie.
