# MediaPipe Setup

## Voraussetzungen

- Python 3.8+
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

### 2. Projekt erstellen

```bash
# Neues Projekt erstellen
uv init media_pipe_demo
cd media_pipe_demo
```

### 3. Dependencies installieren

```bash
# MediaPipe und OpenCV installieren
uv add mediapipe opencv-python
```

ODER direkt im Workshop-Verzeichnis:

```bash
# Im Projektverzeichnis
cd 3_mediapipe_detection

# Dependencies installieren
uv add mediapipe opencv-python
```

### 4. Webcam testen

Unter Python:
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
uv add mediapipe
```

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

- Siehe [`usage.md`](usage.md) für das Prompt-Playbook
- Code-Beispiele: [`beispiele/`](beispiele/)
