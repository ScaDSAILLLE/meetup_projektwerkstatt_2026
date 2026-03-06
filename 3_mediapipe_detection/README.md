# MediaPipe – Prompt-Playbook

Dieser Bereich zeigt, wie klassische Computer-Vision(CV)-Pipelines mit MediaPipe aufgebaut sind.
MediaPipe arbeitet mit vortrainierten Echtzeit-Modellen (Face, Hands, Pose) und liefert Landmarken,
die du direkt für Interaktionen, Gestensteuerung und einfache Prototypen nutzen kannst.
OpenCV übernimmt dabei den Video-Input, die Bildvorverarbeitung und das Rendering der Overlays im Fenster.
Die Kombination ist stark, weil OpenCV den stabilen Frame-Loop liefert und MediaPipe darauf präzise CV-Inferenz in Echtzeit ausführt.
Der Fokus liegt auf schneller lokaler Ausführung per Webcam und einem klaren Einstieg in Detection-Workflows.

## Setup

- Anleitung: [`setup.md`](setup.md)

## Tags

- mediapipe
- hand-tracking
- pose-estimation
- face-detection
- prompt-playbook

## Usage

### Überblick

MediaPipe ist ein Framework von Google für Echtzeit-Computer-Vision. In diesem Projekt findest du Beispiele für:
- Face Detection
- Hand Tracking
- Pose Estimation

### Win11 Quickstart (Ausfuehren)

```powershell
uv venv .venv
.venv\Scripts\activate
uv sync

uv run python beispiele/face_detection.py
```

Fallback bei Python-Problemen:

```powershell
uv venv .venv --python 3.11
```

Nutze die Befehle im Ordner `3_mediapipe_detection/`, nicht in `beispiele/`.

Wenn du lieber ein eigenes Entry-Script `app.py` nutzt:

```powershell
uv run python app.py
```

---

### Die Beispiel-Codes

Alle Beispiele liegen in [`beispiele/`](beispiele/):

```
beispiele/
├── face_detection.py     # Einfache Gesichtserkennung
├── hand_tracking.py     # Hand-Tracking mit Gesten
└── pose_estimation.py   # Körperhaltung erkennen
```

---

### Prompt-Playbook für MediaPipe

### 1. Code verstehen

**Im Plan-Modus starten!**

```
Erkläre mir was Mediapipe ist/
Erkläre mir, was OpenCV ist.
```

```
Erkläre mir wie @beispiele/face_detection.py funktioniert.
Was macht die detect_faces() Funktion?
```

### 2. Eigene Idee entwickeln

**Im Plan-Modus:**

```
Wir wollen eine App bauen, die per Handgesten
Mausbewegungen simuliert. Kannst du einen
Plan erstellen, wie wir das umsetzen können?
```

```
Wir wollen eine App bauen, die per Handgesten
den Browser öffnet. Kannst du einen
Plan erstellen, wie wir das umsetzen können?
```

```
Wir wollen eine App bauen, die per Handgesten
die Lautstärke am PC lauter und leiser machen kann. Kannst du einen
Plan erstellen, wie wir das umsetzen können?
```

### 3. Features erweitern

**Zum Beispiel:**

```
In @beispiele/hand_tracking.py wird die Hand erkannt.
Erweitere den Code so, dass bei einer Faust
ein "Klick"-Event ausgegeben wird.
```

### 4. Neues Modell hinzufügen

```
Ich möchte zusätzlich zu Hands auch Face Mesh
nutzen. Zeige mir einen Plan, wie wir beides
kombinieren können.
```

### 5. Debugging

```
In @beispiele/pose_estimation.py gibt es einen Fehler
bei der Anzeige der Skeleton-Linien. Kannst du
den Code prüfen und den Bug fixen?
```

---

### Workflow-Vorschlag

### Phase 1: Verstehen (10 min)

1. Starte OpenCode
2. Frage:
   ```
   Erkläre mir die Struktur von @beispiele/hand_tracking.py
   ```
3. Lass dir den Code erklären

### Phase 2: Ausprobieren (15 min)

1. Führe die Beispiele aus
2. Teste mit deiner Webcam
3. Dokumentiere was funktioniert

### Phase 3: Erweitern (30 min)

1. Wechsle in Plan-Modus (`Tab`)
2. Beschreibe deine Idee:
   ```
   Ich möchte die Hand-Tracking-App erweitern:
   - Wenn Daumen und Zeigefinger sich berühren = Klick
   - Wenn Hand offen = Mausbewegung aktiv
   - Wenn Faust = Maus nicht bewegen
   
   Zeig mir einen Plan!
   ```
3. Iteriere mit Feedback

### Phase 4: Bauen (30 min)

1. Wechsle zu Build-Modus (`Tab`)
2. Sag: "Go ahead and make the changes!"
3. Teste das Ergebnis

---

### Nützliche Prompts

### "Was kann ich damit machen?"

```
Was sind typische Use-Cases für Hand-Tracking
mit MediaPipe? Nenne 5 Beispiele mit kurzer
Beschreibung.
```

### "Wie optimiere ich?"

```
Der Code in @beispiele/pose_estimation.py
läuft langsam. Was kann ich tun, um die
Performance zu verbessern?
```

### "Wie integriere ich das in meine App?"

```
Ich habe eine Flask-Web-App. Zeig mir einen
Plan, wie ich das Hand-Tracking als
WebSocket-Stream einbinden kann.
```

---

### Best Practices

### 1. Starte im Plan-Modus
- Keine versehentlichen Änderungen
- Besserer Code durch Iteration / "Task-Following"

### 2. Referenziere existierenden Code
- `@beispiele/hand_tracking.py` macht es einfacher für OpenCode

### 3. Sei spezifisch bei Gesten
- ❌ "Mach irgendwas mit der Hand"
- ✅ "Wenn Daumen und Zeigefinger sich berühren → Klick"

### 4. Nutze UV
- Statt `pip install` → `uv add <paket>` od. `uv pip install <paket>`

### 5. Teile Fehlermeldungen
- Copy & Paste Fehler in den Prompt
- OpenCode kann helfen zu debuggen

---

### Erweiterungsideen

### Für Fortgeschrittene

1. **Maus-Steuerung** – Handbewegungen → Mausposition
2. **Touchless UI** – GUI per Geste steuern
3. **Präsenz-Erkennung** – Ist jemand am Arbeitsplatz?
4. **Fitness-App** – Übungskorrektur
5. **Musik-Steuerung** – Lauter/leiser per Geste
6. **Virtuelle Tastatur** – Typen in der Luft

### Mit VLMs kombinieren

- MediaPipe erkennt Hand → VLM interpretiert Geste
- Siehe [`4_qwen_vl_scene/`](../4_qwen_vl_scene/)

---

### Mehr Infos

- MediaPipe Docs: https://ai.google.dev/edge/mediapipe/solutions/guide?hl=de
- MediaPipe GitHub: https://github.com/google/mediapipe
- OpenCV: https://opencv.org/

---

### Troubleshooting

### "cv2.imshow funktioniert nicht"
→ Nutze `cv2.imwrite()` zum Speichern oder nutze eine Display-Alternative

### "Webcam wird nicht erkannt"
→ Prüfe `cv2.VideoCapture(0)` – 0 ist die erste Kamera

### "Langsam auf CPU"
→ MediaPipe ist optimiert, aber teste niedrigere Auflösung

---

### Weiter geht's

- Theoretischer Hintergrund: [`2_computer_vision_intro/`](../2_computer_vision_intro/)
- Tool-Setup: [`1_opencode/`](../1_opencode/)
