# Qwen3.5 / Qwen-VL Scene Understanding Setup

## Voraussetzungen

- Ollama (lokal installiert) und/oder KIARA API Key (für heute bereits vorbereitet)
- Python 3.10+
- Bilddateien für Analyse (oder Webcam)

## Installation

### 1. Ollama installieren

> s. Ollama-Website: https://ollama.com/


### 2. Modell herunterladen

```bash
# qwen3.5:0.8b ist klein und läuft auf CPU
ollama pull qwen3.5:0.8b
```

**Alternativen:**
```bash
# Größere Modelle (brauchen mehr RAM)
siehe: https://ollama.com/search?c=vision
```

### 3. Python-Dependencies

```bash
# UV prüfen
uv --version

# Falls nicht installiert:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Projekt erstellen
uv venv .venv
.venv\Scripts\activate
uv sync
```

---

## KIARA API (optional)

Wenn du den Remote-Zugang nutzen willst, setze den Key als
System-Umgebungsvariable (z. B. via `setup.bat`). Es wird **keine** `.env` benötigt.

- Base URL: `https://kiara.sc.uni-leipzig.de/api/v1`
- Modell: `qwen3-vl-30b-a3b-instruct`
- Env-Var: `KIARA_API_KEY` (ist bereits gesetzt!)

Optional kannst du die Base URL mit `KIARA_API_BASE` überschreiben.

---

## Modell-Info

### qwen3.5:0.8b

| Eigenschaft | Wert |
|-------------|------|
| Größe | ~1 GB |
| RAM-Bedarf | ~2-3 GB |
| CPU-only | ✅ Ja |
|推理zeit | ~3-10s/Bild |

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
ollama run qwen3.5:0.8b "Describe this image: /path/to/image.jpg"
```

### Python-Test

```bash
uv run beispiele/scene_understanding.py /pfad/zum/bild.jpg
```

```python
import ollama

response = ollama.chat(
    model='qwen3.5:0.8b',
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
uv run beispiele/scene_understanding.py /pfad/zum/bild.jpg \
  --backend kiara \
  --kiara-model qwen3-vl-30b-a3b-instruct
```

---

## Troubleshooting

### "Ollama not found"

- Ollama zum PATH hinzufügen
- Oder: `ollama serve` in separatem Terminal starten

### "Model not found"

> ggf. Ollama updaten / neu installieren (es gab zuletzt bugs... insb. bei Windows-Versionen.)
```bash
ollama list
ollama pull qwen3.5:0.8b
```

### "Out of memory"

- Bildgröße reduzieren
- Unwahrscheinlich bei 0.8B Modell :)

### "Zu langsam"

- Normal bei CPU-only
- Kleinere Bilder verwenden
- Quantisierte Modelle nutzen

---

## Nächste Schritte

- Siehe [`README.md`](README.md) für das Prompt-Playbook
- Code-Beispiele: [`beispiele/`](beispiele/)
