# Qwen VL Scene Understanding – Prompt-Playbook

## Setup

- Anleitung: [`setup.md`](setup.md)

## Tags

- qwen-vl
- kiara-api
- ollama
- scene-understanding
- prompt-playbook

## Usage

### Überblick

In diesem Projekt nutzen wir **Qwen VL** lokal via Ollama oder remote via **KIARA API**.
Das Modell kann:
- Bilder beschreiben
- Objekte erkennen
- Fragen zu Bildern beantworten
- Szenen analysieren

---

### Die Beispiel-Codes

Alle Beispiele liegen in [`beispiele/`](beispiele/):

```
beispiele/
└── scene_understanding.py   # Bildanalyse mit qwen3-vl
```

### Lokal vs. KIARA API

Der Beispiel-Code kann entweder lokal (Ollama) oder via KIARA API laufen.

**Lokal (Ollama):**
```bash
python beispiele/scene_understanding.py /pfad/zum/bild.jpg
```

**KIARA API:**
```bash
python beispiele/scene_understanding.py /pfad/zum/bild.jpg \
  --backend kiara \
  --kiara-model qwen3-vl-30b-a3b-instruct
```

Voraussetzung: `KIARA_API_KEY` ist als System-Umgebungsvariable gesetzt
(z. B. via `setup.bat`). Optional: `KIARA_API_BASE` zum Überschreiben der Base-URL.
Es wird **keine** `.env` benötigt.

---

### Prompt-Playbook für VLMs

### 1. Code verstehen

**Im Plan-Modus starten!**

```
Erkläre mir wie @beispiele/scene_understanding.py funktioniert.
Was macht die analyze_image() Funktion?
```

### 2. Eigene Idee entwickeln

**Im Plan-Modus:**

```
Wir wollen eine App bauen, die Live-Webcam-Bilder
analysiert und beschreibt, was gerade passiert.
Kannst du mir einen Plan zeigen?
```

### 3. Features erweitern

**Zum Beispiel:**

```
In @beispiele/scene_understanding.py wird ein Bild
analysiert. Erweitere den Code so, dass er bei
einer Person im Bild "Person erkannt" ausgibt.
```

### 4. Mit MediaPipe kombinieren

```
MediaPipe erkennt Hand-Landmarks. Wie können wir
qwen3-vl nutzen, um die erkannte Geste in
natürlicher Sprache zu beschreiben?
```

### 5. Debugging

```
Der Code in @beispiele/scene_understanding.py
gibt einen Fehler zurück. Kannst du den Code
prüfen und den Bug fixen?
```

---

### Workflow-Vorschlag

### Phase 1: Verstehen (10 min)

1. Starte OpenCode
2. Frage:
   ```
   Erkläre mir die Struktur von @beispiele/scene_understanding.py
   ```
3. Lass dir den Code erklären

### Phase 2: Ausprobieren (15 min)

1. Führe die Beispiele aus
2. Teste mit eigenen Bildern
3. Dokumentiere was funktioniert

### Phase 3: Erweitern (30 min)

1. Wechsle in Plan-Modus (`Tab`)
2. Beschreibe deine Idee:
   ```
   Ich möchte die Bildanalyse erweitern:
   - Analysiere das Bild auf Objekte
   - Wenn eine Person erkannt wird, sag "Person"
   - Wenn ein Hund erkannt wird, sag "Hund"
   - Gib die Ergebnisse als JSON zurück
   
   Zeig mir einen Plan!
   ```
3. Iteriere mit Feedback

### Phase 4: Bauen (30 min)

1. Wechsle zu Build-Modus (`Tab`)
2. Sag: "Go ahead and make the changes!"
3. Teste das Ergebnis

---

### Nützliche Prompts

### "Was siehst du?"

```
Was ist in diesem Bild zu sehen? Beschreibe
die Hauptelemente und die Stimmung.
```

### "Was ist das für eine Person?"

```
Analysiere die Person im Bild: Alter, Kleidung,
Haltung. Was könnte sie tun?
```

### "Erkenne Objekte"

```
Liste alle erkennbaren Objekte im Bild auf.
```

### "Vergleiche Bilder"

```
Vergleiche diese beiden Bilder. Was ist
gleich, was ist unterschiedlich?
```

---

### Best Practices

### 1. Starte im Plan-Modus
- Keine versehentlichen Änderungen
- Besserer Code durch Iteration

### 2. Referenziere existierenden Code
- `@beispiele/scene_understanding.py` macht es einfacher für OpenCode

### 3. Sei spezifisch bei Prompts
- ❌ "Was ist das?"
- ✅ "Erkenne alle Personen im Bild und beschreibe ihre Kleidung"

### 4. Nutze UV
- Statt `pip install` → `uv add <paket>`

### 5. Bilder vorher verkleinern
- CPU ist langsam – kleinere Bilder = schnellere Antwort

### 6. Sei geduldig
- ~3-5 Sekunden pro Bild auf CPU ist normal

---

### Erweiterungsideen

### Für Fortgeschrittene

1. **Live-Analyse** – Webcam-Bilder in Echtzeit analysieren
2. **Objekt-Zählung** – Wie viele X sind im Bild?
3. **Text-Erkennung** – Text im Bild lesen
4. **Stimmungs-Analyse** – Was ist die Atmosphäre?
5. **Qualitätskontrolle** – Fehler in Produktbildern erkennen
6. **Accessibility** – Bildbeschreibungen für Blinde generieren

### Mit MediaPipe kombinieren

- MediaPipe erkennt Pose/Hand → VLM interpretiert
- Siehe [`3_mediapipe_detection/`](../3_mediapipe_detection/)

---

### Mehr Infos

- Ollama: https://ollama.ai/
- Qwen VL: https://qwenlm.github.io/
- Ollama Python API: https://github.com/ollama/ollama-python

---

### Performance-Tipps

| Problem | Lösung |
|---------|--------|
| Zu langsam | Bild auf 512x512 oder kleiner |
| Out of Memory | Kleineres Modell (2b statt 7b) |
| Falsche Ergebnisse | Prompts klarer formulieren |
| Keine Antwort | Ollama läuft? `ollama serve` |

---

### Troubleshooting

### "ollama not running"
→ `ollama serve` in separatem Terminal starten

### "connection refused"
→ Ollama ist nicht gestartet

### "model not found"
→ `ollama pull qwen3-vl:2b`

---

### Weiter geht's

- Theoretischer Hintergrund: [`2_computer_vision_intro/`](../2_computer_vision_intro/)
- Tool-Setup: [`1_opencode/`](../1_opencode/)
- MediaPipe: [`3_mediapipe_detection/`](../3_mediapipe_detection/)
