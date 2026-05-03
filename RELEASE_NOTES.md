# 📋 Release Notes — Automation Execution Agent

---

## v1.0.0 — Initiële Release
*Datum: mei 2026*

### 🎉 Eerste versie

Dit is de eerste publieke release van de Automation Execution Agent.

### ✅ Wat is inbegrepen

**Server (Replit)**
- Flask webserver met live dashboard
- GPT-4o Vision integratie voor schermanalyse
- Excel upload en verwerking (`.xlsx` en `.xls`)
- Live screenshot weergave in de browser
- AI vraag-en-antwoord systeem via web interface
- Start / Pauzeer / Hervat / Stop bediening
- Voortgangsbalk en statistieken per rij
- Activiteiten log (laatste 20 berichten)

**Lokale Agent (Windows/Mac/Linux)**
- Automatische screenshots elke 2 seconden
- PyAutoGUI voor muisklikken en toetsenbordinvoer
- Tesseract OCR voor tekst herkenning op scherm
- Failsafe: muis naar hoek = onmiddellijk stoppen
- Verbindingstest bij opstarten
- Automatisch herstarten bij tijdelijke verbindingsfout

**Web Interface**
- Volledig responsief — werkt op desktop, tablet, iPhone en iPad
- Donker thema (OLED-vriendelijk)
- Excel upload direct vanuit iOS Bestanden-app
- Toevoegbaar aan beginscherm als PWA

### 📱 Apparaatondersteuning
- ✅ Windows 10/11 (lokale agent + web interface)
- ✅ macOS 12+ (lokale agent + web interface)
- ✅ Linux Ubuntu/Debian (lokale agent + web interface)
- ✅ iPhone iOS 15+ (web interface / afstandsbediening)
- ✅ iPad iPadOS 15+ (web interface / afstandsbediening)
- ✅ Android 10+ (web interface / afstandsbediening)

### ⚠️ Bekende beperkingen
- Gratis Replit-accounts slapen na ~30 minuten inactiviteit
- OCR is minder nauwkeurig zonder Tesseract installatie
- Geen wachtwoordbeveiliging op de web interface (gebruik een verborgen URL)
- Multi-monitor ondersteuning nog niet beschikbaar
- Geen persistente workflow-opslag (herstart = schone lei)

### 🔧 Vereisten
- Python 3.11 of hoger
- OpenAI API key (GPT-4o toegang)
- Replit account (gratis of betaald)

---

## Geplande versies

### v1.1.0 — Workflow opslaan
- Geleerde stappen opslaan als herbruikbare workflow
- Workflow exporteren en importeren (JSON)
- Stap-voor-stap preview van opgeslagen workflows

### v1.2.0 — Demonstratiemodus
- AI demonstreert elke stap voordat hij uitvoert
- Gebruiker kan stap goedkeuren of aanpassen
- Leereffect: systeem wordt slimmer per iteratie

### v1.3.0 — Goedkeuringsmodus
- Elke actie vereist expliciete goedkeuring
- Ideaal voor gevoelige of foutgevoelige workflows
- Goedkeuringslog voor auditing

### v1.4.0 — Geplande uitvoering
- Stel in wanneer de agent automatisch start
- Dagelijkse / wekelijkse herhalingen
- E-mail of push notificatie bij voltooiing

### v1.5.0 — Multi-monitor
- Ondersteuning voor meerdere schermen
- Kies welk scherm de agent gebruikt
- Splitscreen weergave in de web interface

### v2.0.0 — Volledig autonome modus
- Agent werkt volledig zelfstandig zonder menselijke tussenkomst
- Automatische foutherstel
- Gedetailleerde rapportage per sessie
- Integratie met externe systemen (webhook, e-mail, etc.)

---

## Bijdragen

Heb je een bug gevonden of een idee? Open een issue of stuur een pull request op GitHub.

---

*Automation Execution Agent — gebouwd voor mensen die hun tijd beter kunnen besteden.*
