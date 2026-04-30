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

## Quickstart im Workshop

Hinweis: nutzt hierfür gerne schon Opencode und lasst euch das alles erklären!
Für Entwickler:innen: fühlt euch frei unter Quellenangabe ein eigenes Setup auf diesem Projekt zu erarbeiten. :)

### 1) Abhängigkeiten installieren

```bash
uv sync
```

### 2) LiteRT-LM-Server starten

```bash
uv run uvicorn litert_lm_server:app --host 0.0.0.0 --port 8000
```

### 3) Chat-App starten (neues Terminal)

```bash
uv run python app.py
```

### 4) Ausprobieren

- Stelle eine reine Textfrage.
- Lade ein Bild hoch und lass es analysieren.
- Lade Audio hoch oder nutze das Mikrofon.

## Aha-Effekt: Lokaler Agent ohne Internet

Für den Workshop ist das ein starker Moment:

1. Starte Server und App wie oben.
2. Öffne die Chatoberfläche im Browser.
3. Schalte auf dem Windows-Workshop-Laptop das WLAN aus.
4. Stelle erneut Fragen.

Wenn alles korrekt lokal läuft, funktioniert der Agent weiterhin. Genau das macht „lokal“ greifbar.

## Mit OpenCode erklären lassen

Nutze OpenCode direkt als Coach im Projekt:

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


