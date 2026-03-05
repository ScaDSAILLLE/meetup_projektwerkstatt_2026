# Qwen VL Scene Understanding Setup

## Voraussetzungen

- Ollama (lokal installiert) oder KIARA API Key
- Python 3.8+
- Bilddateien für Analyse (oder Webcam)

## Installation

### 1. Ollama installieren

**Windows (PowerShell):**
```powershell
curl -L -o ollama-installer.exe https://ollama.ai/install.bat
.\ollama-installer.exe
```

**macOS / Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Modell herunterladen

```bash
# qwen3-vl:2b ist klein und läuft auf CPU
ollama pull qwen3-vl:2b
```

**Alternativen:**
```bash
# Größere Modelle (brauchen mehr RAM)
ollama pull llava
ollama pull llava:7b
```

### 3. Python-Dependencies

```bash
# UV prüfen
uv --version

# Projekt erstellen
uv init vlm_demo
cd vlm_demo

# Dependencies installieren
uv add ollama requests pillow python-dotenv
```

ODER im Workshop-Verzeichnis:

```bash
cd 4_qwen_vl_scene

uv add ollama requests pillow python-dotenv
```

---

## KIARA API (optional)

Wenn du den Remote-Zugang nutzen willst, setze den Key als
System-Umgebungsvariable (z. B. via `setup.bat`). Es wird **keine** `.env` benötigt.

- Base URL: `https://kiara.sc.uni-leipzig.de/api/v1`
- Modell: `qwen3-vl-30b-a3b-instruct`
- Env-Var: `KIARA_API_KEY`

Optional kannst du die Base URL mit `KIARA_API_BASE` überschreiben.

---

## Modell-Info

### qwen3-vl:2b

| Eigenschaft | Wert |
|-------------|------|
| Größe | ~2 GB |
| RAM-Bedarf | ~4 GB |
| CPU-only | ✅ Ja |
|推理zeit | ~3-5s/Bild |

### Fähigkeiten

- Bildbeschreibung
- Objekterkennung (textuell)
- Text-in-Bild lesen
- Szenenverständnis
- Fragen beantworten

---

## Testen

### CLI-Test

```bash
ollama run qwen3-vl:2b "Describe this image: /path/to/image.jpg"
```

### Python-Test

```python
import ollama

response = ollama.chat(
    model='qwen3-vl:2b',
    messages=[{
        'role': 'user',
        'content': 'What is in this image?',
        'images': ['/path/to/image.jpg']
    }]
)

print(response['message']['content'])
```

### KIARA API Test

Voraussetzung: `KIARA_API_KEY` ist gesetzt.

```bash
python beispiele/scene_understanding.py /pfad/zum/bild.jpg \
  --backend kiara \
  --kiara-model qwen3-vl-30b-a3b-instruct
```

---

## Troubleshooting

### "Ollama not found"

- Ollama zum PATH hinzufügen
- Oder: `ollama serve` in separatem Terminal starten

### "Model not found"

```bash
ollama list
ollama pull qwen3-vl:2b
```

### "Out of memory"

- Bildgröße reduzieren
- Kleineres Modell nutzen (qwen3-vl:2b statt 8b)

### "Zu langsam"

- Normal bei CPU-only
- Kleinere Bilder verwenden
- Quantisierte Modelle nutzen

---

## Nächste Schritte

- Siehe [`README.md`](README.md) für das Prompt-Playbook
- Code-Beispiele: [`beispiele/`](beispiele/)
