# Computer Vision – Einführung

## Was ist Computer Vision?

Computer Vision (CV) ist ein Teilgebiet der Künstlichen Intelligenz, das Computern ermöglicht, visuelle Informationen aus Bildern und Videos zu verstehen. Das umfasst:

- **Objekterkennung** (Object Detection)
- **Bildsegmentierung** (Semantic/Instance Segmentation)
- **Gesichtserkennung** (Face Detection/Recognition)
- **Pose-Estimation** (Körperhaltung erkennen)
- **Hand-Tracking** (Handgesten erkennen)
- **Scene Understanding** (Szenen verstehen)

---

## Pose & Gesture Detection

### Pose Estimation

Pose Estimation identifiziert die Position von Körpergelenken in Bildern oder Videos. Die wichtigsten Modelle:

| Modell | Anbieter | Besonderheiten |
|--------|----------|----------------|
| MediaPipe Pose | Google | Schnell, Multi-Person |
| OpenPose | CMU | Detailliert, Ganzkörper |
| MoveNet | Google | Ultra-schnell, Sport |

**Anwendungsbeispiele:**
- Fitness-Apps (Übungskorrektur)
- Gestensteuerung
- Posturanalyse
- Motion Capture

### Gesture Detection

Handgesten erkennen:

| Modell | Anbieter | Besonderheiten |
|--------|----------|----------------|
| MediaPipe Hands | Google | 21 Landmarks, Echtzeit |
| Handtrack.js | - | JavaScript, Browser |
| MediaPipe Holistics | Google | Face + Hands + Pose |

**Anwendungsbeispiele:**
- Touchless UI-Steuerung
- Virtuelle Maus per Webcam
- Übersetzungs-Apps (Gebärdensprache)
- Signatur-Erkennung

---

## MediaPipe – Das Schweizer Taschenmesser

MediaPipe ist ein Framework von Google mit vortrainierten Modellen für:

- **Face Detection** – Gesichter finden
- **Face Mesh** – 468 Gesichtspunkte
- **Hands** – 21 Hand-Landmarks pro Hand
- **Pose** – 33 Körper-Landmarks
- **Object Detection** – Objekte (mit Boxen)

### Warum MediaPipe?

✅ **Open Source** – Kostenlos nutzbar  
✅ **Cross-Platform** – Python, JS, C++, Android, iOS  
✅ **Echtzeitfähig** – Läuft flüssig auf CPUs  
✅ **Vortrainiert** – Kein Training nötig  
✅ **Vielseitig** – Von Face bis Object Detection  

---

## Vision Language Models (VLMs)

### Was sind VLMs?

VLMs kombinieren Computer Vision mit Large Language Models. Sie können:

- Bilder beschreiben
- Fragen zu Bildern beantworten
- Objekte lokalisieren
- Szenen verstehen

### Wie haben VLMs die Use-Cases verändert?

**Traditionelle CV → VLM-basierte Ansätze:**

| Traditionell | VLM-basiert |
|--------------|-------------|
| Spezifisches Modell pro Task | Ein Modell für alles |
| Gelabelte Daten nötig | Natural Language Instructions |
| Batch-Verarbeitung | Interaktive Abfragen |
| API-basiert | Lokal lauffähig (Ollama) |

### Lokale VLMs mit Ollama

Mit Ollama können VLMs lokal auf der CPU laufen:

- **qwen3-vl:2b** – Klein, schnell, gut für CPU
- **llava** – Bekanntes VLM für lokale Nutzung
- **phi4-vision** – Microsoft's VLM

### Use-Cases für VLMs

- **Interaktive Bildanalyse** – "Was passiert in diesem Bild?"
- **Datengenerierung** – Labels für andere Modelle erstellen
- **Accessibility** – Bildbeschreibungen für Blinde
- **Qualitätskontrolle** – Automatische Fehlererkennung

---

## CPU vs GPU – Was geht lokal?

### Erwartungen für CPU-only

| Modell | RAM-Bedarf | Geschwindigkeit |
|--------|------------|-----------------|
| MediaPipe (Face) | ~100 MB | Echtzeit |
| MediaPipe (Hands) | ~200 MB | Echtzeit |
| MediaPipe (Pose) | ~200 MB | Echtzeit |
| Ollama qwen3-vl:2b | ~2 GB | Langsam (~2-5s/Bild) |

### Optimierungstipps

1. **MediaPipe:** Läuft nativ sehr effizient – kein Problem
2. **VLMs:** Kleine Modelle wählen (2b statt 8b+)
3. **Batch-Verarbeitung:** Nicht echtzeit, aber machbar
4. **Quantisierung:** Modelle mit Q4/Q5 nutzen

---

## Werkzeuge in diesem Workshop

### MediaPipe (Beispiel 1)

Siehe [`3_mediapipe_detection/`](../3_mediapipe_detection/)

- Face Detection
- Hand Tracking
- Pose Estimation

### VLM mit Ollama (Beispiel 2)

Siehe [`4_qwen_vl_scene/`](../4_qwen_vl_scene/)

- qwen3-vl:2b
- Scene Understanding
- Bildanalyse

---

## Weiterführende Ressourcen

### MediaPipe
- https://google.github.io/mediapipe/
- https://github.com/google/mediapipe

### VLMs & Ollama
- https://ollama.ai/
- https://qwenlm.github.io/

### Pose Detection
- https://google.github.io/mediapipe/solutions/pose
- https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md

---

## Nächste Schritte

1. **Tool-Setup:** [`1_opencode/setup.md`](../1_opencode/setup.md)
2. **Prompt-Playbook:** [`1_opencode/usage.md`](../1_opencode/usage.md)
3. **MediaPipe starten:** [`3_mediapipe_detection/`](../3_mediapipe_detection/)
4. **VLM ausprobieren:** [`4_qwen_vl_scene/`](../4_qwen_vl_scene/)
