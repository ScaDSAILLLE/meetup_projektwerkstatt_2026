# Dein lokaler multimodaler KI-Agent mit Gemma 4

Hast du schon immer mal überlegt oder dir gewünscht, deinen eigenen kleinen lokalen Offline-KI-Agenten zu betreiben, der Text, Bild, Audio und perspektivisch sogar Video versteht? Das ist möglich: mit Googles Gemma-4-Modellen (Open Source, Apache-2.0, also auch kommerziell nutzbar) und einer lokalen LiteRT-LM-Basis.

In diesem Workshop-Ordner findest du eine kleine multimodale Demo-App samt eigenem lokalem Server. Das Ziel ist, dass du nicht nur zuschaust, sondern direkt selbst startest, verstehst, erweiterst und daraus deinen eigenen lokalen Agenten baust.

## Warum das spannend ist

- **Lokal statt Cloud-Zwang**: Anfragen und Medien bleiben auf deinem Gerät: was das an Möglichkeiten eröffnet, oder?
- **Datensouveränität**: Du entscheidest selbst, was verarbeitet wird und wo.
- **Multimodal**: Ein Setup für Text, Bilder und Audio in einer Pipeline: Gemma4 ist wirklich gut und auch die kleinen Modelle (e2b & e4b) laufen zuverlässig. Probiere es aus!
- **Agentisches Potenzial**: Daraus lassen sich Tool-Calls und lokale Automationen auf deinem PC entwickeln. Cool oder? Fällt dir direkt etwas ein?

Hinweis zur Einordnung: Debatten rund um Features wie MSFT Recall haben gezeigt, wie sensibel lokales Kontextverständnis sein kann. Genau deshalb ist es wichtig, Technik praktisch zu verstehen, bewusst zu konfigurieren und kontrolliert einzusetzen.
Nachlese:
- [Heise.de - Erste-Erfahrungen-mit-Recall](https://www.heise.de/news/Erste-Erfahrungen-mit-Recall-9750138.html)
- [Heise.de Microsoft-rudert-angeblich-bei-KI-Plänen-zurück](https://www.heise.de/news/Microsoft-rudert-angeblich-bei-KI-Plaenen-zurueck-11213718.html)

KI ist nützlich und erleichtert sicher einiges. Trotzdem sollten wir wohl genauer hinschauen, wie wir das ganze nutzen und einbinden wollen und auf was (Stichwort eigene Daten) wir Zugriff geben möchten/sollten!
Rein lokale (offline) Setups bringen hier eigentlich alles mit, was es braucht, um sowas eigens, sicher und konfigierbar zu betreiben. Aktuelle Modelle (LLMs/VLMs/MLLMs) sind selbst in kleineren Größen mittlerweile zu wirklich nützlichen Dingen im Stande. Probiert es hier gerne mal mit einem der neuesten Modelle aus. :)

## Was in diesem Ordner gezeigt wird

- `litert_lm_server.py`: Lokaler OpenAI-kompatibler API-Server auf FastAPI-Basis mit LiteRT-LM-Engine.
- `app.py`: Gradio-Chatoberfläche mit multimodalem Input (Text, Bild, Audio, Mikrofon).
- `pyproject.toml`: Abhängigkeiten und Projektkonfiguration.

Die App sendet Medien nur im aktuellen Turn und nutzt danach kompakten Textkontext für Folgefragen. So bleibt der Verlauf effizient und nachvollziehbar.

## Workshop-Ziel

Am Ende solltest du:

- das lokale multimodale Setup angesehen und getestet haben,
- die Demo selbst starten und bedienen können,
- versucht haben, eine eigene Erweiterung zu ergänzen.

Viel Spaß beim Bauen deines eigenen lokalen KI-Agenten...

## Nutzung:

Wir haben heute bereits alles für dich aufgesetzt (denn: die neuesten Bibliotheken machen nunmal gerne Ärger).
Wenn du es eigens aufsetzen willst, scrolle runter zum Kapitel **Setup**.

**Hinweis:** Damit gemma4 *multimodal* auf so ziemlich "jeder Kiste" läuft mit diesem Setup (ja, auch Raspberry Pi läuft echt gut und passebel schnell zu mitlesen, schaut mal [hier](https://ai.google.dev/edge/litert-lm?hl=de)), musste das Kontextfenster auf die letzten 6 Nachrichten begrenzt werden. Beachtet das bitte. Fragt im Zweifel mal Opencode, wo das *eingestellt* wird im Code und wie man das Kontextfenster vergrößern kann ;)

### 0) Terminal in `2_test_gemma4_multimodal` öffnen, WSL Instanz starten:

Unter Windows führen wir alles in WSL aus. 
Nutze den Rechtsklick auf den Ordner `2_test_gemma4_multimodal` und wähle `Open in integrated Terminal`
Gib nun folgendes ein:

```bash
wsl
```

**Das brauchst du im folgenden für all deine *Terminals*.**


### 1) Starten des LiteRT-LM Servers:

Der Server wird mit folgendem Befehl gestartet:

```bash
export HF_HOME="./huggingface-hub"
export LITERT_MODEL_PATH="./huggingface-hub/hub/models--litert-community--gemma-4-E4B-it-litert-lm/snapshots/28299f30ee4d43294517a4ac93abd6163412f07f/gemma-4-E4B-it.litertlm"
export LITERT_BACKEND="CPU"
uv run uvicorn litert_lm_server:app --host 0.0.0.0 --port 8000
```

Sofern keine Fehlermeldungen kommen, läuft der Server nach einer kleinen Weile und steht bereit für anfragen.

### 2) Starten der Chat-App:

Parallel kannst du nun schon die app.py starten. Warte aber am besten, bis der Server läuft. 
Gib diesen Befehl zum starten der app.py ein:

```bash
uv run python app.py
```

Wenn die app.py läuft wird in etwa sowas angezeigt: 

```bash
* Running on local URL:  http://0.0.0.0:7860
* To create a public link, set `share=True` in `launch()`.
```

**Klicke nun auf den Link *http://0.0.0.0:7860* oder öffne im Browser die Seite *localhost:7860*.**
Damit erreichst du die lokal-laufende App. 

### 3) Probier es aus:

- Stelle eine reine Textfrage.
- Lade ein Bild hoch und lass es analysieren.
- Lade Audio hoch oder nutze das Mikrofon.

Viel Spaß beim testen. :)

## Kleiner *Aha*-Effekt: Lokaler Agent ohne Internet

Teste doch mal *ohne Internetverbindung*

1. Starte Server und App wie oben.
2. Öffne die Chatoberfläche im Browser.
3. Schalte auf dem Windows-Workshop-Laptop das WLAN aus.
4. Stelle erneut Fragen.

Wenn alles korrekt lokal läuft, funktioniert der Agent weiterhin: also vollkommen lokal!
Ist doch cool oder? 

## Mit OpenCode erklären lassen

Nutze nun OpenCode direkt als *Coach* im Projekt:

- „Erkläre mir `app.py` Schritt für Schritt: Wie werden Bild und Audio in API-Content umgewandelt?“
- „Zeige mir, wie `litert_lm_server.py` OpenAI-Requests zu LiteRT-LM mapped.“
- „Welche Stellen muss ich ändern, um Tool-Calls einzubauen?“
- „Hilf mir, ein lokales Dateisystem-Tool sicher anzubinden.“

So lernst du nicht nur das Was, sondern auch das Warum hinter jeder Komponente.

## Ideen zum Erweitern

- **Tool-Calls**: z. B. Dateien auflisten, Notizen strukturieren, lokale Infos abfragen.
- **PC-Workflows**: Automatisierte Aufgaben wie Zusammenfassungen, Sortierung, Voranalysen.
- **Prompt-Playbooks**: Wiederverwendbare Rollen und Arbeitsanweisungen für verschiedene Aufgaben.
- **UI-Verbesserungen**: Eigene Buttons, Modusumschalter, Session-Steuerung, Debug-Ansichten.
- **Guardrails**: Grenzen, Rechte und Protokollierung klar definieren.

---

## Setup - *Falls du es dir eigens aufsetzen willst, hier der Step-by-Step Guide:*

*Hinweis: nutze hierfür gerne auch Opencode und lass dir jeden Schritt erklären!*

### 0) Terminal öffnen, repo clonen, in den Ordner `meetup_projektwerkstatt_2026/2_test_gemma4_multimodal` wechseln und WSL starten:

```bash
git clone https://github.com/ScaDSAILLLE/meetup_projektwerkstatt_2026.git
cd meetup_projektwerkstatt_2026/2_test_gemma4_multimodal
```

Nutzt das bitte unter Linux! Also unter Windows alles in **WSL** ausführen:

```bash
wsl
```

MacOS wurde nicht getestet :-| 

### 1) WSLs Ubuntu-Software-Packaged updaten und ggf. nötige Software installieren:

```bash
sudo apt update
sudo apt install -y libgles2 libegl1 libgl1
```

### 2) Abhängigkeiten installieren

```bash
uv sync
```

### 3) HuggingFace & lokales Gemma4-Modell vorbereiten)

Gemma4-Modelle sind auf Hugging Face gated. Bitte einmalig:

1. Bei Hugging Face einloggen (falls nötig Account erstellen)
2. Modellseite öffnen und Terms akzeptieren (falls vorhanden; bei den litert-community-Modellen sollte das nicht nötig sein!)
3. Access Token erstellen (siehe [Huggingface Docs zu Access Tokens](https://huggingface.co/docs/hub/security-tokens))
4. Lokal authentifizieren, wie folgt:

Optional, falls CLI fehlt:

```bash
uv add "huggingface_hub[cli]"
```

Login prüfen:

```bash
uv run hf auth whoami
```

Login durchführen (falls nötig):

```bash
uv run hf auth login
```

**Hier kommt jetzt dein eigens erstelltes HuggingFace Access Token rein**... und fertig: nun kannst du über deinen Account und per CLI Modelle (uvm.) von HuggingFace laden. :)

Lokales Cache-Verzeichnis setzen:

```bash
export HF_HOME="./huggingface-hub"
```

### 4) LiteRT-LM Installation kurz testen

LiteRT-LM installieren (sollte systemweit sein, nicht nur in der *venv*!):

```bash
uv tool install litert-lm
```

Testlauf (lädt Modell bei Bedarf und prüft Runtime):

```bash
litert-lm run --from-huggingface-repo=litert-community/gemma-4-E4B-it-litert-lm gemma-4-E4B-it.litertlm --prompt="Hello, who are you?"
```

Wenn das funktioniert, ist das Setup in der Regel korrekt.

### 5) Modell herunterladen (E4B Beispiel)

Das Modell landet mit `HF_HOME` im Cache unter `./huggingface-hub/hub/...`.

```bash
HF_HOME="./huggingface-hub" uv run hf download litert-community/gemma-4-E4B-it-litert-lm gemma-4-E4B-it.litertlm
```

Den exakten Pfad zur Datei kannst du so ausgeben:

```bash
HF_HOME="./huggingface-hub" uv run python -c "from huggingface_hub import hf_hub_download; print(hf_hub_download(repo_id='litert-community/gemma-4-E4B-it-litert-lm', filename='gemma-4-E4B-it.litertlm'))"
```

### 5) LiteRT-LM-Server starten

`LITERT_MODEL_PATH` auf den Snapshot-Pfad (siehe im Pfad: `<snapshot-id>`!) setzen (aus dem vorherigen Befehl):

```bash
uv run uvicorn litert_lm_server:app --host 0.0.0.0 --port 8000
```

*optional* Umgebungsvariablen setzen:
```bash
export HF_HOME="./huggingface-hub"
export LITERT_MODEL_PATH="./huggingface-hub/hub/models--litert-community--gemma-4-E4B-it-litert-lm/snapshots/<snapshot-id>/gemma-4-E4B-it.litertlm"
export LITERT_BACKEND="CPU"
uv run uvicorn litert_lm_server:app --host 0.0.0.0 --port 8000
```

### 6) Chat-App starten (zweites WSL-Terminal)

```bash
uv run python app.py
```

*optional* Umgebungsvariablen setzen:
```bash
export LOCAL_LLM_BASE_URL="http://localhost:8000/v1"
export LOCAL_LLM_MODEL="gemma-4-E4B-it"
uv run python app.py
```

### 7) Ausprobieren

- Stelle eine reine Textfrage.
- Lade ein Bild hoch und lass es analysieren.
- Lade Audio hoch oder nutze das Mikrofon.