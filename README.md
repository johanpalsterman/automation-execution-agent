# Automation Execution Agent

Een AI-gestuurde automatiseringstool die repetitieve taken uitvoert door je scherm te bekijken en contextueel te handelen — zoals een mens, maar dan 24/7.

## Hoe het werkt

```
[Excel met referenties] → [Replit web app] ←→ [Windows agent op jouw PC]
                                ↓
                        [AI analyseert scherm]
                                ↓
                        [Instructies uitvoeren]
```

1. Je laadt een Excel op met referenties (kolom 1) en waarden (kolom 2)
2. De Windows agent stuurt continu screenshots naar de Replit server
3. De AI ziet het scherm, begrijpt de interface en geeft instructies
4. De Windows agent voert de instructies uit (klikken, typen, etc.)
5. Bij twijfel stelt de AI een vraag die jij beantwoordt via de web interface

---

## Stap 1: Replit opzetten

### 1.1 Nieuwe Replit aanmaken
1. Ga naar [replit.com](https://replit.com) en maak een account
2. Klik op **+ Create Repl**
3. Kies **Python** als template
4. Geef het een naam (bijv. `automation-agent`)

### 1.2 Bestanden uploaden
Upload de volgende bestanden naar je Replit project:
- `app.py`
- `requirements.txt`
- Map `templates/` met daarin `index.html`

### 1.3 OpenAI API Key instellen
1. Ga in Replit naar **Secrets** (sleutel-icoontje in de zijbalk)
2. Voeg toe:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** jouw OpenAI API key (van [platform.openai.com](https://platform.openai.com))

### 1.4 Starten
1. Klik op **Run**
2. De web interface verschijnt — kopieer de URL (bijv. `https://automation-agent.jouw-naam.replit.app`)

---

## Stap 2: Windows Agent installeren

### 2.1 Python installeren
Download Python 3.11+ van [python.org](https://python.org) als je het nog niet hebt.

### 2.2 Dependencies installeren
Open Command Prompt en voer uit:
```
pip install pyautogui pillow requests pytesseract pygetwindow
```

### 2.3 Tesseract OCR installeren (aanbevolen)
Voor betere tekst-herkenning op het scherm:
1. Download van: https://github.com/UB-Mannheim/tesseract/wiki
2. Installeer met standaard instellingen
3. Zorg dat `tesseract` in je PATH staat

### 2.4 Agent configureren
Open `agent.py` in Kladblok en pas regel 1 aan:
```python
REPLIT_URL = "https://automation-agent.jouw-naam.replit.app"
```
(Vervang door jouw echte Replit URL)

### 2.5 Agent starten
```
python agent.py
```

---

## Stap 3: Excel voorbereiden

Maak een Excel bestand met minimaal 2 kolommen:

| Referentie    | Waarde          |
|---------------|-----------------|
| REF-001       | BTW-BE123456789 |
| REF-002       | BTW-BE987654321 |
| KLANT-2024-05 | info@bedrijf.be |

- **Rij 1:** Headers (worden overgeslagen)
- **Kolom A:** De referentie om op te zoeken
- **Kolom B:** De waarde om in te vullen

---

## Stap 4: Gebruik

1. ✅ Replit app draait
2. ✅ `python agent.py` draait op je Windows PC
3. ✅ Open de Replit web interface in je browser
4. Upload je Excel bestand
5. Klik **▶ Start**
6. De agent begint automatisch!

### Tijdens de uitvoering
- Je ziet het scherm van je PC live in de web interface
- De AI beschrijft elke stap in de log
- Als de AI een vraag heeft, verschijnt die in de interface — typ je antwoord en stuur op
- Je kunt op **⏸ Pauzeer** klikken om tijdelijk te stoppen

---

## Veiligheid

- **PyAutoGUI Failsafe:** Beweeg je muis snel naar de **linkerbovenhoek** van je scherm om de agent onmiddellijk te stoppen
- De agent kan niet op eigen initiatief starten — altijd via de web interface

---

## Problemen oplossen

| Probleem | Oplossing |
|----------|-----------|
| Agent kan niet verbinden | Controleer of REPLIT_URL correct is in agent.py |
| AI vindt veld niet | Geef meer context via de feedback interface |
| Screenshots komen niet aan | Controleer firewall / Windows Defender |
| Tesseract fout | Zorg dat Tesseract geïnstalleerd en in PATH staat |

---

## Toekomstige uitbreidingen (roadmap)

- [ ] Fase 2: AI demonstreert aan mens
- [ ] Fase 3: Stap-voor-stap goedkeuring
- [ ] Fase 4: Periodieke controle modus
- [ ] Fase 5: Volledig automatisch
- [ ] Workflow opslaan en hergebruiken
- [ ] Multi-monitor ondersteuning
- [ ] Video opname van uitvoering
