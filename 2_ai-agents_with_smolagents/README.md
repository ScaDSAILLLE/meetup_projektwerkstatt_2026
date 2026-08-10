# KI-Projektwerkstatt: Agenten und Multi-Agentensysteme mit SmolAgents

Angewandte KI. Hands-on. Offen für alle.

In dieser Projektwerkstatt probierst du eine kleine Gradio-App aus, die mit Hugging Face `smolagents` ein Multi-Agentensystem baut. Die App zeigt einen Orchestrator-Agenten, der Aufgaben an spezialisierte Sub-Agenten delegiert, und einzelne Agenten, die du unabhängig testen kannst.

## Worum geht's?

Viele Coding-Agenten wirken zunächst abstrakt: Sie schreiben Code, aber was kann man damit konkret bauen? Dieses Repo gibt dir ein überschaubares Beispiel: eine App, in der Agenten Tools nutzen, Dateien erzeugen und im Team arbeiten.

Du kannst:

- die Demo-App starten und mit den Agenten chatten,
- die Struktur von Gradio-App, Orchestrator und Sub-Agenten nachvollziehen,
- mit OpenCode gezielt Code erklären oder ändern lassen,
- einen eigenen Agenten bauen oder die App um einen Agenten erweitern.

## Was die App zeigt

- `app.py`: Einstiegspunkt der Gradio-App.
- `gradio_ui/welcome_tab.py`: Einstieg und Arbeitsauftrag in der App.
- `gradio_ui/individual_agents_tab.py`: direkte Chats mit einzelnen Agenten.
- `gradio_ui/multimodal_chat_tab.py`: Chat mit dem Orchestrator-Agenten.
- `agents/orchestrator.py`: zentraler `ToolCallingAgent` mit `managed_agents`.
- `agents/image_generator.py`: Flyer-Agent mit Bildgenerierung, Text-Overlay und PDF-Export.
- `agents/agent_workshop.py`: Workshop-Agent für Markdown, Präsentationen und Code-Beispiele.

## Setup

```bash
uv sync
cp .env.example .env
uv run app.py
```

Trage in `.env` deinen `SCADSAI_API_KEY` ein. Die App liest `.env` automatisch über `config.py`; sie muss nicht im Code geöffnet werden.

Öffne danach: <http://localhost:7860>

## Ausprobieren

Starte mit diesen Prompts:

- `Welche Aufgaben kannst du?`
- `Generiere einen Flyer zum Thema KI-Agenten in der Forschung.`
- `Erstelle einen kurzen Workshop zum Thema SmolAgents.`
- `Erstelle eine Präsentation und ein kleines Python-Beispiel zu Multi-Agentensystemen.`

Die App schreibt generierte Bilder und PDFs nach `runtime_data/generated_images/`. Workshop-Dateien wie Markdown, Präsentationen und Code-Beispiele landen in `runtime_data/output/`.

## Tutorial

Für die Projektphase gibt es eine geführte Arbeitsstrecke in [`tutorial.md`](tutorial.md). Sie ist auf etwa 45 Minuten aktive Arbeit ausgelegt und passt damit gut in einen 60–90-minütigen Workshop mit Einstieg, Ausprobieren und freier Erweiterung.

## Mit OpenCode arbeiten

Nutze OpenCode als Coach im Repo, zum Beispiel mit diesen Prompts:

- „Erkläre mir die Architektur dieser App anhand von `app.py`, `gradio_ui/multimodal_chat_tab.py` und `agents/orchestrator.py`."
- „Zeige mir, wie ich einen neuen SmolAgents-Agenten unter `agents/` ergänze."
- „Hilf mir, einen einfachen Quiz-Agenten als neuen Sub-Agenten einzubauen."
- „Prüfe meine Änderung und nenne mir den kleinsten sinnvollen Verifikationsbefehl."

## Links

- [ScaDS.AI Dresden/Leipzig](https://scads.ai/)
- [ScaDS.AI Living Lab](https://scads.ai/living-lab/)
- [Hugging Face SmolAgents](https://huggingface.co/docs/smolagents/index)
- [OpenCode](https://opencode.ai/)

## Lizenz

Workshop-Material: CC BY 4.0  
Code: MIT-Lizenz
