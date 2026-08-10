# Tutorial: Einen eigenen Agenten mit SmolAgents bauen

Dieses Tutorial ist für die aktive und freie Arbeit als Input wärhrend der Projektwerkstatt Session gedacht. Es ist kein vollständiger Kurs, sondern ein geführter Einstieg in Agents und Multi-Agentensystem mit SmolAgents: App ausprobieren, Code verstehen, einen kleinen Agenten bauen und optional in das Multi-Agentensystem einhängen.

Wenn du dich einlesen willst, findest du hier einen hervorragenden Kurs sowie die offizielle Dokumentation von SmolAgents (von HuggingFace):

- Docs: https://huggingface.co/docs/smolagents/index
- Agents Course von HuggingFace: https://huggingface.co/learn/agents-course/unit0/introduction
- SmolAgents-Site mit Beispielen: https://smolagents.org/de/

Wir empfehlen SmolAgents, da es einen super Einstieg in das Thema gibt, die Bibliothek wirklich Anfänger:innen bis fortgeschrittenen-freundlich ist und zudem sehr gut dokumentiert ist.

**Viel Spaß** 

## Ziel

Am Ende hast du:

- die Demo-App gestartet,
- den Unterschied zwischen Einzel-Agent und Orchestrator verstanden,
- einen vorhandenen Agenten direkt getestet,
- einen eigenen Agenten entworfen oder eingebaut,
- OpenCode genutzt, um Code erklären und ändern zu lassen.

## 0. Vorbereitung

✅ **...haben wir für das Meetup schon für dich erledigt! Wenn du es nach dem Meetup nochmal testen willst, hast du heir die nötigen Setup-Schritte. :)** 

```bash
uv sync
cp .env.example .env
uv run app.py
```

Trage in `.env` deinen `SCADSAI_API_KEY` ein. Öffne danach <http://localhost:7860>.

Wenn der Chat meldet, dass `SCADSAI_API_KEY` fehlt, ist die App selbst erreichbar, aber die Agenten können noch nicht mit dem Modell sprechen.

## 1. App ausprobieren

Teste zuerst den Tab **Einzelne Agenten**.

Prompts für den Flyer-Agenten:

- `Generiere einen Flyer zum Thema KI-Agenten in der Projektwerkstatt.`
- `Erstelle daraus auch eine PDF-Datei.`

Prompts für den Workshop-Agenten:

- `Schreibe einen kurzen Workshop-Text zu SmolAgents als Markdown.`
- `Erstelle eine Präsentation und ein Python-Beispiel zu Multi-Agentensystemen.`

Wechsle danach zum Tab **Orchestrator Chat**.

Prompts für den Orchestrator:

- `Welche Aufgaben kannst du?`
- `Erstelle einen Workshop zum Thema Agenten und generiere danach einen Flyer dafür.`
- `Welche Sub-Agenten stehen dir zur Verfügung?`

Beobachte: Beim Orchestrator entscheidet ein Agent, welcher Sub-Agent die Aufgabe bekommt. Bei den Einzel-Agenten sprichst du direkt mit dem jeweiligen Spezialisten.

## 2. Code-Struktur verstehen

Öffne mit OpenCode diese Dateien und lass sie dir erklären:

- `app.py`: baut die Gradio-App und hängt die Tabs ein.
- `gradio_ui/individual_agents_tab.py`: direkte Chats mit einzelnen Agenten.
- `gradio_ui/multimodal_chat_tab.py`: Chat mit dem Orchestrator und Streaming der Zwischenschritte.
- `agents/orchestrator.py`: erstellt den zentralen Agenten mit `managed_agents`.
- `agents/image_generator.py`: Flyer-Agent mit Tools für Prompt, Bild, Text-Overlay und PDF.
- `agents/agent_workshop.py`: Workshop-Agent mit Tools für Dateien, Präsentationen und Code-Check.

Wichtige Opencode Funktionen/Befehle & gute OpenCode-Prompts:

- Nutze zu Beginn in Projekten gerne `/init`- dann ließt der Agent sich durch das Repository und legt eine AGENTS.md mit grundlegenden Infos zum Projekt an, wenn nicht schon vorhanden. Diese kann in kommenden Sessions dann wieder gelesen und Agents so *"ge-onboardet"* werden. Clever!
- „Erkläre mir `agents/orchestrator.py` Schritt für Schritt. Was sind `managed_agents`?"
- „Welche Tools hat der Flyer-Agent und in welcher Reihenfolge werden sie typischerweise genutzt?"
- „Wo müsste ich einen dritten Agenten registrieren?"
- „Welche Dateien darf ich anfassen, wenn ich nur die UI-Texte ändern will?"

## 3. SmolAgents-Grundidee

Ein Agent in dieser App besteht aus drei Teilen:

- KI-Modell (LLM/VLM): hier ein OpenAI-kompatibles ScaDS.AI-Modell über [TUD:AI HPC Service](llm.scads.ai).
- Tools: Python-Funktionen mit `@tool`, die der Agent aufrufen darf.
- Instruktionen: Beschreibung, Rolle und gewünschter Arbeitsablauf. (Das ist im Grunde Prompt-Engineering; ggf. könnte man sogar sagen Context-Engineering zus. mit den Tools.)

Ein Multi-Agentensystem entsteht, wenn ein Agent andere Agenten als `managed_agents` bekommt. Der Orchestrator muss die Arbeit dann nicht selbst erledigen, sondern kann passende Spezialisten beauftragen. Das ist ein klassisches Beispiel für eine Triage- od. Routing-Agent Struktur. Man kann Agents aber verschieden orchestrieren. [Hier eine Beispielquelle dazu](https://vercel.com/i/agent-orchestration-patterns).

## 4. Mini-Aufgabe: Eigenen Agenten planen

Wähle eine kleine Rolle für einen Agenten. Fällt dir was ein? Was wäre ein nützlicher Agent mit einer klaren Aufgabe?

Beispiele:

- Quiz-Agent: erstellt drei Verständnisfragen zu einem Thema.
- Ideen-Agent: sammelt Projektideen und sortiert sie nach Aufwand.
- Agenda-Agent: erstellt einen 45-Minuten-Workshopplan.
- Glossar-Agent: erklärt Fachbegriffe kurz und verständlich.

Skizziere für deinen Agenten:

- Name des Agenten
- Aufgabe in einem Satz
- 1–2 Tools, falls nötig
- Beispielprompt
- erwartetes Ergebnis

## 5. Mini-Aufgabe: Agent als Datei ergänzen

Lege einen neuen Agenten unter `agents/` an, zum Beispiel `agents/quiz_agent.py`.

Eine einfache Struktur:

```python
from __future__ import annotations

from smolagents import OpenAIServerModel, ToolCallingAgent, tool

import config


@tool
def create_quiz(topic: str) -> str:
    """Erstellt drei kurze Quizfragen zu einem Thema.

    Args:
        topic: Thema für das Quiz.
    """
    return (
        f"Quiz zum Thema {topic}:\n"
        "1. Was ist die wichtigste Grundidee?\n"
        "2. Welches Beispiel passt dazu?\n"
        "3. Wo liegen mögliche Grenzen?"
    )


def create_agent() -> ToolCallingAgent:
    if not config.SCADSAI_API_KEY:
        raise RuntimeError("SCADSAI_API_KEY is not set.")

    model = OpenAIServerModel(
        model_id=config.SCADSAI_CHAT_MODEL,
        api_base=config.SCADSAI_API_BASE,
        api_key=config.SCADSAI_API_KEY,
        tool_choice="auto",
    )
    return ToolCallingAgent(
        tools=[create_quiz],
        model=model,
        name="quiz_generator",
        description="Erstellt kurze Quizfragen zu einem Thema.",
        instructions="Du bist ein Quiz-Agent. Nutze create_quiz für Quizfragen.",
        max_steps=5,
    )
```

Prüfe danach:

```bash
uv run python -m compileall agents # ...prüft auf syntaktische Fehler im Code.
```

## 6. Optional: Agent in die App integrieren

Wenn dein Agent direkt im Orchestrator auftauchen soll:

- Importiere seine Factory in `agents/orchestrator.py`.
- Erstelle den Agenten in `create_orchestrator()`.
- Ergänze ihn in `managed_agents=[...]`.
- Aktualisiere die Orchestrator-Instruktionen und die UI-Copy.

Wenn dein Agent zusätzlich als Einzel-Agent testbar sein soll:

- Ergänze ihn in `gradio_ui/individual_agents_tab.py`.
- Baue dafür einen eigenen `gr.ChatInterface`-Block.

Lass dir von OpenCode den kleinsten Patch vorschlagen:

```text
Ich habe agents/quiz_agent.py erstellt. Integriere den Agenten minimal in den Orchestrator und in den Einzel-Agenten-Tab. Ändere nur die nötigen Dateien.
```

## 7. Verifizieren

Nutze nach Änderungen mindestens:

```bash
uv run python -m compileall app.py config.py agents gradio_ui
```
Das prüft vor dem Start auf sog. synthaktische Fehler, also Fehler in der Codeschreibweise. 

Starte danach die App neu und teste deinen Agenten mit einem einfachen Prompt. (`uv run app.py`) ;)

## 8. Freie Erweiterungen

Wenn du früher fertig bist:

- Baue einen Agenten, der Workshop-Ideen nach Aufwand sortiert.
- Ergänze einen Agenten, der aus einem Thema eine Agenda erstellt.
- Verbessere die Prompts der vorhandenen Agenten.
- Erweitere die UI um Beispielprompts oder kurze Hilfetexte.
- Baue bewusst Guardrails ein: Welche Dateien darf ein Agent lesen oder schreiben?

Ziel ist nicht Perfektion oder das alles sauber läuft: Ziel ist, dass du den Weg von Python-Funktion zu Tool, von Tool zu Agent und von Agent zu Multi-Agentensystem einmal selbst gegangen bist.
**Viel Erfolg!**
