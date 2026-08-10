"""Multimodal Chat Tab -- Chat-Oberfläche für den Orchestrator-Agent.

Diese Registerkarte verbindet die Gradio-UI mit dem Orchestrator-Agenten.
Der Orchestrator verwaltet Sub-Agenten (Flyer-Generator, Workshop-Generator)
und kann Meta-Fragen beantworten sowie Aufgaben delegieren.

Features:
- **Streaming**: Zwischenschritte des Agenten (Tool-Aufrufe, Logs, Bilder)
  werden in Echtzeit im Chat angezeigt.
- **Datei-Anzeige**: Generierte Dateien (Bilder, PDFs, PowerPoints) werden
  direkt im Chat als Vorschau bzw. Download-Karte angezeigt.
"""

from __future__ import annotations

import mimetypes
import re
from pathlib import Path
from typing import Any

import gradio as gr
from smolagents.gradio_ui import pull_messages_from_step
from smolagents.memory import ActionStep, FinalAnswerStep, PlanningStep

from agents.orchestrator import create_orchestrator

#: Singleton -- wird bei erster Nutzung erstellt.
_orchestrator: Any = None

#: Cache für Initialisierungsfehler, damit nicht bei jedem Call
#: neu versucht wird, einen kaputten Agent zu bauen.
_init_error: Exception | None = None

#: Datei-Endungen, die im Chat als Vorschau/Download angezeigt werden.
_KNOWN_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".pptx", ".md", ".py", ".txt", ".json"}

#: Regex für Dateipfade mit bekannten Endungen.  Erfasst sowohl absolute
#: Pfade (``/home/user/output/file.png``) als auch relative
#: (``output/file.pptx``).
_FILE_PATTERN = re.compile(
    r"[\w./\\-]+\.(?:png|jpg|jpeg|webp|gif|pdf|pptx|md|py|txt|json)",
    re.IGNORECASE,
)


def _get_orchestrator() -> Any:
    """Lazily initialize the orchestrator agent (singleton pattern).

    Returns the cached orchestrator instance, creating it on first call.
    """
    global _orchestrator, _init_error
    if _orchestrator is not None:
        return _orchestrator
    if _init_error is not None:
        raise _init_error
    try:
        _orchestrator = create_orchestrator()
        return _orchestrator
    except Exception as exc:
        _init_error = exc
        raise


def _extract_file_paths(text: str) -> list[Path]:
    """Extract existing file paths from a text string.

    Scans for paths ending with known extensions (png, jpg, pdf, pptx, ...),
    verifies they exist on disk, and returns them as ``Path`` objects.
    """
    if not text:
        return []
    result: list[Path] = []
    for match in _FILE_PATTERN.findall(text):
        p = Path(match)
        if p.is_file():
            result.append(p)
    return result


def _collect_files_from_memory(agent: Any) -> list[Path]:
    """Collect file paths from the agent's memory steps.

    Scans ``ActionStep.observations`` for file paths returned by tool calls.
    """
    files: list[Path] = []
    memory = getattr(agent, "memory", None)
    if memory is None:
        return files
    for step in memory.steps:
        if isinstance(step, ActionStep):
            obs = getattr(step, "observations", "") or ""
            files.extend(_extract_file_paths(obs))
    return files


def chat(message: str, history: list[Any]) -> Any:
    """Handle a chat message by delegating to the orchestrator agent.

    Streams intermediate agent steps (tool calls, logs, images) in real-time,
    then displays generated files (images, PDFs, PowerPoints) as inline
    previews or download cards.

    Args:
        message: The user's text input.
        history: Conversation history (unused -- the agent manages its
            own memory via ``reset=False``).
    """
    try:
        agent = _get_orchestrator()
    except Exception as exc:
        yield [
            gr.ChatMessage(
                role="assistant",
                content=(
                    f"⚠️ Der Orchestrator konnte nicht initialisiert werden.\n\n"
                    f"Fehler: {exc}\n\n"
                    "Stelle sicher, dass SCADSAI_API_KEY in der .env gesetzt ist."
                ),
            )
        ]
        return

    if not message or not message.strip():
        yield [gr.ChatMessage(role="assistant", content="⚠️ Bitte gib eine Nachricht ein.")]
        return

    all_messages: list[gr.ChatMessage] = []
    final_answer_text = ""

    try:
        for event in agent.run(message, stream=True, reset=False):
            if isinstance(event, FinalAnswerStep):
                final_answer_text = str(getattr(event, "output", ""))
            if isinstance(event, (ActionStep, PlanningStep, FinalAnswerStep)):
                for msg in pull_messages_from_step(event):
                    all_messages.append(msg)
                yield list(all_messages)
    except Exception as exc:
        yield [
            gr.ChatMessage(
                role="assistant",
                content=f"⚠️ Fehler bei der Ausführung des Agenten:\n\n{exc}",
            )
        ]
        return

    # --- Dateien aus finaler Antwort + Agent-Memory extrahieren ---
    found_files = _extract_file_paths(final_answer_text)
    found_files.extend(_collect_files_from_memory(agent))

    # Deduplizieren bei Beibehaltung der Reihenfolge
    seen: set[str] = set()
    unique_files: list[Path] = []
    for fp in found_files:
        key = str(fp.resolve())
        if key not in seen:
            seen.add(key)
            unique_files.append(fp)

    if unique_files:
        for fp in unique_files:
            mime = mimetypes.guess_type(str(fp))[0] or "application/octet-stream"
            all_messages.append(
                gr.ChatMessage(
                    role="assistant",
                    content={"path": str(fp), "mime_type": mime},
                    metadata={"title": f"📎 {fp.name}", "status": "done"},
                )
            )
        yield list(all_messages)


def build_mm_chat_tab() -> None:
    """Build the multimodal chat tab inside the Gradio Blocks context."""
    with gr.Tab("Orchestrator Chat"):
        gr.Markdown(
            """
### Multi-Agenten-Orchestrator

Hier sprichst du mit dem zentralen Orchestrator. Er kennt die verfügbaren
Sub-Agenten, beantwortet Meta-Fragen und delegiert Aufgaben an den passenden
Spezialisten.

| Sub-Agent | Fähigkeiten |
|-----------|-------------|
| **flyer_generator** | Flyer-Bilder generieren, als PDF exportieren |
| **workshop_generator** | Markdown-Texte, PowerPoint-Präsentationen, Python-Code-Beispiele |

Nutze diesen Tab nach dem Test der einzelnen Agenten. So siehst du, was sich
ändert, wenn nicht du selbst den Spezialisten auswählst, sondern ein Agent die
Koordination übernimmt. Zwischenschritte, Tool-Aufrufe und generierte Dateien
werden im Chat angezeigt.

**Beispiele:**
- `Welche Aufgaben kannst du?`
- `Generiere einen Flyer zum Thema KI-Agenten in der Forschung`
- `Erstelle einen Workshop zum Thema SmolAgents`
- `Erstelle einen Workshop und danach einen passenden Flyer dazu`
            """
        )
        gr.ChatInterface(
            fn=chat,
            title="orchestrator",
            description="Stell eine Frage oder gib eine Aufgabe an das Multi-Agentensystem.",
        )
