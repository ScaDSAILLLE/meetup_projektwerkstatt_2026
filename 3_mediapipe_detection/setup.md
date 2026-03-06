# MediaPipe Setup

## Voraussetzungen

- Python 3.11+ (Windows 11)
- Webcam (für Echtzeit-Detection)
- Oder: Bilder/Videos für Offline-Verarbeitung

## Installation

### 1. UV prüfen/installieren

```bash
# Prüfen ob UV installiert
uv --version

# Falls nicht installiert:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Virtuelle Umgebung erstellen (Windows 11)

```powershell
# Im Repo-Ordner 3_mediapipe_detection ausführen
uv venv .venv
.venv\Scripts\activate
```

Hinweis: Führe die Befehle in `3_mediapipe_detection/` aus,
nicht in `3_mediapipe_detection/beispiele/`.

Falls dein Standard-Python nicht kompatibel ist, nutze explizit:

```powershell
uv venv .venv --python 3.11
```

### 3. Dependencies installieren

```bash
# Fuer die klassischen mp.solutions Beispiele
uv sync
```

Hinweis: Die neuere `mediapipe==0.10.32` stellt `mp.solutions`
in diesem Umfeld nicht mehr bereit. Die Beispielskripte basieren
auf der klassischen Solutions-API und nutzen deshalb `0.10.14`.

### 4. Installation verifizieren

```bash
uv run python -c "import mediapipe as mp; print(mp.__version__); print(hasattr(mp, 'solutions')); print(mp.__file__)"
```

Erwartung:
- `hasattr(mp, 'solutions')` muss `True` sein.

### 5. Beispiele starten (stoppen geht mit der Taste "q")

```bash
uv run beispiele/face_detection.py
uv run beispiele/hand_tracking.py
uv run beispiele/pose_estimation.py
```

### 6. Webcam testen

Unter Python: \
> - terminal (cmd / powershell) öffnen \
> - python eingeben und `Enter` klicken, dann: 

```python
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print("Webcam funktioniert!" if ret else "Webcam fehlgeschlagen")
cap.release()
```

---

## Modelle

MediaPipe bietet verschiedene Lösungen:

| Modell | landmarks | Typische Nutzung |
|--------|-----------|------------------|
| Face Detection | 6 | Gesichter finden |
| Face Mesh | 468 | Detail-Gesichtserkennung |
| Hands | 21 | Handgesten |
| Pose | 33 | Körperhaltung |
| Objectron | 3D | 3D-Objekte |

---

## Schnellstart

Siehe [`beispiele/`](beispiele/) für fertige Skripte:

- `face_detection.py` – Einfache Gesichtserkennung
- `hand_tracking.py` – Hand-Tracking
- `pose_estimation.py` – Körperhaltung erkennen

---

## Troubleshooting

### "ImportError: No module named 'mediapipe'"

```bash
uv sync
```

### "AttributeError: module 'mediapipe' has no attribute 'solutions'"

Das ist meist eine fehlerhafte Installation oder ein falsches Environment.

```bash
# venv aktivieren (Windows)
.venv\Scripts\activate

# mediapipe sauber neu installieren
uv remove mediapipe
uv add "mediapipe==0.10.14"

# prüfen, ob solutions verfügbar ist
uv run python -c "import mediapipe as mp; print(mp.__version__); print(hasattr(mp, 'solutions')); print(mp.__file__)"
```

### TensorFlow/absl/protobuf Logs beim Start

Meldungen wie diese sind bei MediaPipe auf Windows oft normal:
- `Created TensorFlow Lite XNNPACK delegate for CPU`
- `Feedback manager requires a model with a single signature inference`
- `SymbolDatabase.GetPrototype() is deprecated`

Solange Webcam-Fenster und Detection laufen, kannst du diese Hinweise ignorieren.

### "VIRTUAL_ENV ... does not match the project environment path"

Das passiert, wenn du in einem anderen venv bist (z. B. in
`3_mediapipe_detection/beispiele/.venv`).

- `deactivate`
- in `3_mediapipe_detection/` wechseln
- `.venv\Scripts\activate`
- dann `uv run python beispiele/pose_estimation.py`

### "OpenCV: cannot access camera"

- Prüfen ob Webcam von anderen Apps genutzt wird
- Unter Linux: `sudo apt install libgl1-mesa-glx`

### "Fehler bei cv2.imshow"

OpenCV kann in manchen Umgebungen kein Fenster öffnen. Alternative:

```python
# Statt cv2.imshow:
cv2.imwrite('output.jpg', frame)
print("Bild gespeichert")
```

---

## Nächste Schritte

- Siehe [`README.md`](README.md) für das Prompt-Playbook
- Code-Beispiele: [`beispiele/`](beispiele/)
