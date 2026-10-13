"""Orchestrator Agent -- zentraler Multi-Agent-Manager.

Der Orchestrator ist ein ``ToolCallingAgent``, der Sub-Agenten als
``managed_agents`` verwaltet. Er bekommt ein System-Prompt mit der
Beschreibung aller verfügbaren Agenten und ihrer Fähigkeiten.

Aufgaben des Orchestrators:

1. **Meta-Fragen beantworten** -- Z.B. "Welche Aufgaben kannst du?"
   gibt eine Übersicht aller verfügbaren Agenten und Fähigkeiten.

2. **Delegation** -- Bei aufgabenbezogenen Anfragen delegiert er an den
   passenden Sub-Agenten (Flyer-Generator, Workshop-Generator).

Der Orchestrator nutzt ``SCADSAI_ORCHESTRATOR_MODEL`` für besseres Reasoning
und Routing.
"""

from __future__ import annotations

import sys
from pathlib import Path

from smolagents import OpenAIServerModel, ToolCallingAgent

try:
    import config
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import config

from agents.agent_workshop import create_agent as _create_workshop_agent
from agents.image_generator import create_agent as _create_flyer_agent


def _require_api_key() -> str:
    key = config.SCADSAI_API_KEY
    if not key:
        raise RuntimeError(
            "SCADSAI_API_KEY is not set. "
            "Copy .env.example to .env and fill in SCADSAI_API_KEY=..."
        )
    return key


ORCHESTRATOR_INSTRUCTIONS = """\
Du bist der Orchestrator-Agent des ScaDS.AI Living Lab. Du bist der \
zentrale Ansprechpartner für Nutzer im Chat.

## Verfügbare Sub-Agenten

1. **flyer_generator** -- Generiert Flyer-Bilder für beliebige Themen.
   - Kann ein Thema zu einem detaillierten Bild-Prompt erweitern
   - Generiert ein Flyer-Bild aus dem enhanced Prompt
   - Konvertiert das generierte Bild in eine PDF-Datei

2. **workshop_generator** -- Generiert Workshop-Materialien.
   - Erstellt Markdown-Texte zu beliebigen Themen
   - Erstellt PowerPoint-Präsentationen aus Markdown
   - Schreibt Python-Code-Beispiele und überprüft diese auf Lauffähigkeit

## Dein Verhalten

- Wenn der Nutzer eine Meta-Frage stellt (z.B. "Was kannst du?", "Welche \
Aufgaben hast du?", "Wer bist du?"), beantworte diese direkt mit einer \
Übersicht deiner Fähigkeiten und der verfügbaren Sub-Agenten.

- Wenn der Nutzer eine aufgabenbezogene Anfrage stellt, delegiere an den \
passenden Sub-Agenten:
  * Flyer/Bild/PDF generieren -> flyer_generator
  * Workshop/Präsentation/Code-Beispiel -> workshop_generator

- Antworte immer auf Deutsch, freundlich und hilfsbereit.

- Wenn du eine Aufgabe an einen Sub-Agenten delegierst, gib dem Sub-Agenten \
eine klare, detaillierte Aufgabenbeschreibung mit.

- Nach der Delegation fasse das Ergebnis des Sub-Agenten für den Nutzer zusammen.

## Wichtig

- Du kannst nicht selbst Bilder generieren oder Präsentationen erstellen. \
Nutze immer die Sub-Agenten.
- Wenn eine Anfrage nicht in den Bereich der Sub-Agenten fällt, erkläre \
höflich, was du tun kannst.
"""


def create_orchestrator() -> ToolCallingAgent:
    """Create and return the configured Orchestrator Agent.

    The orchestrator manages two sub-agents:
    1. Flyer-Generator (image generation + PDF conversion)
    2. Workshop-Generator (markdown, presentations, code examples)

    It uses ``SCADSAI_ORCHESTRATOR_MODEL`` for better reasoning and routing
    capabilities.

    Returns:
        A configured ``ToolCallingAgent`` instance.

    Raises:
        RuntimeError: If ``SCADSAI_API_KEY`` is not set.
    """
    model = OpenAIServerModel(
        model_id=config.SCADSAI_ORCHESTRATOR_MODEL,
        api_base=config.SCADSAI_API_BASE,
        api_key=_require_api_key(),
    )
    # geändert, OW:
    # Kein globales tool_choice am Model setzen. SmolAgents entscheidet pro
    # Request selbst, wann Tools vorhanden sind; einige vLLM-Endpunkte lehnen
    # tool_choice ohne gleichzeitiges tools-Payload sonst mit HTTP 400 ab.
    # Error den ich erhielt beim testen: 
    # [...]
    # Error while parsing tool call from model output: The model output does not contain any JSON blob.
    # [Step 19: Duration 2.95 seconds| Input tokens: 141,628 | Output tokens: 8,472]
    # Reached max steps.
    # [Step 20: Duration 0.18 seconds]

    flyer_agent = _create_flyer_agent()
    workshop_agent = _create_workshop_agent()

    return ToolCallingAgent(
        tools=[],
        model=model,
        managed_agents=[flyer_agent, workshop_agent],
        name="orchestrator",
        description=(
            "Der zentrale Orchestrator-Agent des ScaDS.AI Living Lab. "
            "Verwaltet Sub-Agenten für Flyer-Generierung und Workshop-Erstellung. "
            "Beantwortet Meta-Fragen und delegiert Aufgaben."
        ),
        instructions=ORCHESTRATOR_INSTRUCTIONS,
        max_steps=15,
    )


__all__ = ["create_orchestrator"]


if __name__ == "__main__":
    agent = create_orchestrator()
    response = agent.run("Welche Aufgaben kannst du?")
    print(response)
