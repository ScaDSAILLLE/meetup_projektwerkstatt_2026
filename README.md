# KI-Projektwerkstatt #1 2026

## Computer Vision – Pose & Gesture Detection

Angewandte KI. Hands-on. Offen für alle.

---

## Worum geht's?

Wir starten eine neue, zweimonatliche KI-Projektwerkstatt.  
Ein offenes Workshopformat von 16:00–19:00 Uhr, bei dem ihr an eigenen Ideen arbeitet, neue KI-Themen ausprobiert oder gemeinsam Prototypen baut.

Einmalig teilnehmen oder über das Jahr hinweg kontinuierlich an einem Projekt arbeiten – beides ist möglich.

**Wir stellen:**
- Vorbereitete Workshop-Laptops
- API-Keys & Tokens
- Beispielcode, Repos & Ressourcen
- Raum & Infrastruktur

**Ihr bringt:**
- Ideen – oder einfach Neugier
- Lust auf Ausprobieren
- Optional: eigenes Setup

---

## Format

Nach einer kurzen Einführung und thematischem Input arbeitet ihr selbstständig – allein oder im Team an euren Ideen oder an Beispielen, die wir aufbereiten.  
AI-Pair-Programming und Agentic Coding sind ausdrücklich erwünscht – wir bereiten ein Setup mit u.a. OpenCode vor. Testet es aus, lernt programmieren oder verfeinert euer eigenes Produktiv-Setup.

Zum Abschluss gibt es freiwillige Kurz-Demos (3–5 Minuten) für alle, die zeigen möchten, woran sie gearbeitet haben sowie angeregte Diskussionen zum Thema, zum State-of-the-Art und allem, was noch interessiert.

Freies Kommen und Gehen ist möglich.

---

## Fokusthema: Pose & Gesture Detection mit Computer Vision

Für alle, die noch keine eigene Idee mitbringen oder schon länger mit Computer-Vision-Systemen experimentieren wollten, bieten wir einen thematischen Einstieg:

Wir zeigen, wie sich mit bestehenden Modellen (z. B. MediaPipe) Körperposen und Handgesten erkennen und in einfache Anwendungen überführen lassen. Was können solche spezialisierten Detection-Modelle, wofür kann man sie einsetzen und wie haben sich Use-Cases auch durch das Aufkommen von Vision-Language-Models verändert?

### Mögliche Beispiele:
- Gestensteuerung für Apps/Desktop
- Visuelle Trigger & Kontrollmechanismen
- Explorative Use-Case-Entwicklung

Es stehen vorbereitete Repos für Setup & minimale Startprojekte sowie weiterführende Ressourcen bereit.  
Fokus liegt auf Anwendung, Ideenfindung und schnellem Prototyping.

---

## Über die Reihe

Die Projektwerkstatt findet alle zwei Monate statt.  
Ziel ist es, angewandte KI gemeinsam zu entwickeln – vom Experiment bis zum tragfähigen Projekt.

Entwickelt Ideen bis hin zum Service oder Startup oder nehmt euch Know-how, Code, Kontakte und Erfahrung mit. Auch Unternehmen, Dev-Teams oder Freelancer sind angesprochen, die KI bereits im Alltag erfolgreich einsetzen, kürzlich damit begonnen haben oder vorhaben, dies demnächst zu tun.

---

## Programm

| Zeit | Programm |
|------|----------|
| 15:45 | Doors Open & Ankommen |
| 16:00 | Begrüßung & Vorstellung ScaDS.AI |
| 16:10 | Startup Pitch & Demo: FEED |
| 16:25 | Input: Computer Vision & Pose/Gesture Detection |
| 16:40 | Setup & Ressourcen |
| 16:45–18:15 | Projektphase / Werkstatt |
| 18:15–18:30 | Kurzpräsentationen & Austausch (freiwillig) |
| ab 18:30 | OpenLab, Networking and Demo-Session |

---

## Ressourcen

### Tools

- **OpenCode** – AI-Coding-Agent für Terminal/IDE
  - Siehe [`1_opencode/`](1_opencode/)
  
### Beispielprojekte

- **MediaPipe Detection** – Face, Hand, Pose Detection
  - Siehe [`3_mediapipe_detection/`](3_mediapipe_detection/)
  
- **Vision Language Models** – Scene Understanding mit VLMs
  - Siehe [`4_qwen_vl_scene/`](4_qwen_vl_scene/)

### Theoretischer Input

- **Computer Vision Intro** – Grundlagen und Konzepte
  - Siehe [`2_computer_vision_intro/`](2_computer_vision_intro/)

---

## Setup

### Windows (WSL empfohlen!)

Wir empfehlen die Nutzung von **WSL (Windows Subsystem for Linux)** für die beste Erfahrung mit OpenCode und den KI-Tools.

1. **Setup-Skript** (Windows CMD/PowerShell):
   ```cmd
   .\setup.bat
   ```
   Oder manuell:
   - Ollama installieren: `curl -L -o ollama-installer.exe https://ollama.ai/install.bat`
   - OpenCode in WSL: `curl -fsSL https://opencode.ai/install | bash`
   - UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **API-Keys setzen:**
   - Siehe `.setup_example.bat` für Vorlage
   - Oder direkt in der OpenCode-TUI mit `/connect`

### Ollama Modelle

Für CPU-only Nutzung empfehlen wir:
- `qwen3-vl:2b` – Vision-Language-Modell, läuft auf CPU (~2GB RAM)

Testen mit:
```bash
ollama run qwen3-vl:2b
```

---

## Lizenz

Workshop-Material: CC BY 4.0  
Code: MIT-Lizenz
