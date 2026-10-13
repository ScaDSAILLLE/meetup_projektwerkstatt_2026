"""Direct chat interfaces for the specialized SmolAgents agents."""

from __future__ import annotations

import mimetypes
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import gradio as gr
from smolagents.gradio_ui import pull_messages_from_step
from smolagents.memory import ActionStep, FinalAnswerStep, PlanningStep

from agents.agent_workshop import create_agent as create_workshop_agent
from agents.image_generator import create_agent as create_flyer_agent

_agents: dict[str, Any] = {}
_init_errors: dict[str, Exception] = {}
_FILE_PATTERN = re.compile(
    r"[\w./\\-]+\.(?:png|jpg|jpeg|webp|gif|pdf|pptx|md|py|txt|json)",
    re.IGNORECASE,
)


def _get_agent(name: str, factory: Callable[[], Any]) -> Any:
    if name in _agents:
        return _agents[name]
    if name in _init_errors:
        raise _init_errors[name]
    try:
        agent = factory()
    except Exception as exc:
        _init_errors[name] = exc
        raise
    _agents[name] = agent
    return agent


def _extract_file_paths(text: str) -> list[Path]:
    if not text:
        return []
    result: list[Path] = []
    for match in _FILE_PATTERN.findall(text):
        path = Path(match)
        if path.is_file():
            result.append(path)
    return result


def _collect_files_from_memory(agent: Any) -> list[Path]:
    files: list[Path] = []
    memory = getattr(agent, "memory", None)
    if memory is None:
        return files
    for step in memory.steps:
        if isinstance(step, ActionStep):
            observations = getattr(step, "observations", "") or ""
            files.extend(_extract_file_paths(observations))
    return files


def _chat_with_agent(name: str, factory: Callable[[], Any], message: str) -> Any:
    try:
        agent = _get_agent(name, factory)
    except Exception as exc:
        yield [
            gr.ChatMessage(
                role="assistant",
                content=(
                    f"Der Agent `{name}` konnte nicht initialisiert werden.\n\n"
                    f"Fehler: {exc}\n\n"
                    "Stelle sicher, dass `SCADSAI_API_KEY` in `.env` gesetzt ist."
                ),
            )
        ]
        return

    if not message or not message.strip():
        yield [gr.ChatMessage(role="assistant", content="Bitte gib eine Nachricht ein.")]
        return

    all_messages: list[gr.ChatMessage] = []
    final_answer_text = ""
    try:
        for event in agent.run(message, stream=True, reset=False):
            if isinstance(event, FinalAnswerStep):
                final_answer_text = str(getattr(event, "output", ""))
            if isinstance(event, (ActionStep, PlanningStep, FinalAnswerStep)):
                all_messages.extend(pull_messages_from_step(event))
                yield list(all_messages)
    except Exception as exc:
        yield [
            gr.ChatMessage(
                role="assistant",
                content=f"Fehler bei der Ausführung des Agenten `{name}`:\n\n{exc}",
            )
        ]
        return

    found_files = _extract_file_paths(final_answer_text)
    found_files.extend(_collect_files_from_memory(agent))

    seen: set[str] = set()
    unique_files: list[Path] = []
    for file_path in found_files:
        key = str(file_path.resolve())
        if key not in seen:
            seen.add(key)
            unique_files.append(file_path)

    if unique_files:
        for file_path in unique_files:
            mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            all_messages.append(
                gr.ChatMessage(
                    role="assistant",
                    content={"path": str(file_path), "mime_type": mime},
                    metadata={"title": file_path.name, "status": "done"},
                )
            )
        yield list(all_messages)


def chat_flyer(message: str, history: list[Any]) -> Any:
    """Chat directly with the flyer generator agent."""
    del history
    yield from _chat_with_agent("flyer_generator", create_flyer_agent, message)


def chat_workshop(message: str, history: list[Any]) -> Any:
    """Chat directly with the workshop generator agent."""
    del history
    yield from _chat_with_agent("workshop_generator", create_workshop_agent, message)


def build_individual_agents_tab() -> None:
    """Build a tab for testing each managed agent without the orchestrator."""
    with gr.Tab("Einzelne Agenten"):
        gr.Markdown(
            """
### Spezialisten direkt testen

Hier sprichst du ohne Orchestrator direkt mit den einzelnen Agenten. Das ist im Workshop hilfreich, um zu sehen, was ein Spezialist selbst kann und was erst durch Orchestrierung entsteht.
            """
        )

        with gr.Accordion("Flyer-Agent", open=True):
            gr.Markdown(
                """
Der Flyer-Agent erzeugt ein Flyer-Bild zu einem Thema, rendert deutschen Text mit den Living-Lab-Schriften auf das Bild und kann das Ergebnis als PDF exportieren.

Beispiel: `Generiere einen Flyer zum Thema KI-Agenten in der Forschung und exportiere ihn als PDF.`
                """
            )
            gr.ChatInterface(
                fn=chat_flyer,
                title="flyer_generator",
                description="Direkter Chat mit dem Flyer-Agenten.",
            )

        with gr.Accordion("Workshop-Agent", open=False):
            gr.Markdown(
                """
Der Workshop-Agent erstellt Markdown-Texte, PowerPoint-Präsentationen und Python-Code-Beispiele. Generierte Dateien landen in `runtime_data/output/`.

Beispiel: `Erstelle einen kurzen Workshop zu SmolAgents mit Präsentation und Python-Beispiel.`
                """
            )
            gr.ChatInterface(
                fn=chat_workshop,
                title="workshop_generator",
                description="Direkter Chat mit dem Workshop-Agenten.",
            )
