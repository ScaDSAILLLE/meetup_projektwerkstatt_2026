"""Welcome tab for the SmolAgents Projektwerkstatt app."""

from __future__ import annotations

import gradio as gr

WELCOME_TEXT = """
## Willkommen zur SmolAgents Projektwerkstatt

Diese App ist ein praktischer Einstieg in KI-Agenten und Multi-Agentensysteme. Du kannst einzelne Spezial-Agenten testen und danach sehen, wie ein Orchestrator Aufgaben an diese Agenten delegiert.

### Was du hier ausprobieren kannst

- **Einzelne Agenten**: Sprich direkt mit dem Flyer-Agenten oder dem Workshop-Agenten.
- **Orchestrator Chat**: Gib eine Aufgabe an den zentralen Agenten und beobachte, welchen Sub-Agenten er einsetzt.
- **Tool-Nutzung**: Sieh, wie Agenten Python-Funktionen als Werkzeuge verwenden und Dateien erzeugen.
- **Erweiterung mit OpenCode**: Lass dir die Struktur erklären und baue einen eigenen Agenten dazu.

### Vorschlag für die nächsten Schritte

1. Öffne **Einzelne Agenten** und teste beide Spezialisten.
2. Öffne **Orchestrator Chat** und frage: `Welche Aufgaben kannst du?`
3. Lies `tutorial.md` und lass dir die genannten Dateien von OpenCode erklären.
4. Ergänze einen kleinen eigenen Agenten oder ändere die vorhandenen Agenten.

### Beispielprompts

- `Generiere einen Flyer zum Thema KI-Agenten in der Projektwerkstatt.`
- `Erstelle einen kurzen Workshop zum Thema SmolAgents.`
- `Welche Sub-Agenten stehen dir zur Verfügung?`
- `Erstelle einen Workshop und danach einen passenden Flyer dafür.`

Generierte Bilder und PDFs landen in `runtime_data/generated_images/`. Workshop-Dateien landen in `runtime_data/output/`.
"""


def build_welcome_tab() -> None:
    with gr.Tab("Welcome"):
        gr.Markdown(WELCOME_TEXT)
