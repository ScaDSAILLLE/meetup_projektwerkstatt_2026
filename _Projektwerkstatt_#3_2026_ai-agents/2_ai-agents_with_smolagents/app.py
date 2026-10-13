"""SmolAgents workshop app for the ScaDS.AI Projektwerkstatt.

Run from the starter root::

    uv sync
    uv run app.py

Then open http://localhost:7860.

The UI shows four tabs:

- **Welcome** -- workshop introduction and suggested path
- **Einzelne Agenten** -- direct chats with the specialized agents
- **Orchestrator Chat** -- multi-agent chat through the orchestrator
- **About** -- context, acknowledgements, links

Architecture: UI in ``app.py`` + ``gradio_ui/``, business logic in
``agents/``, env-driven config in ``config.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make repo-local imports work when this file is run
# directly (``python app.py``).
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gradio as gr

import config
from gradio_ui.about_tab import build_about_tab
from gradio_ui.header import render_global_header
from gradio_ui.individual_agents_tab import build_individual_agents_tab
from gradio_ui.multimodal_chat_tab import build_mm_chat_tab
from gradio_ui.welcome_tab import build_welcome_tab


def build_demo() -> gr.Blocks:
    with gr.Blocks(
        fill_height=True,
        title="ScaDS.AI Living Lab Demo",
    ) as demo:
        render_global_header(
            title="SmolAgents Projektwerkstatt",
            tagline="Agenten bauen, einzeln testen und als Multi-Agentensystem orchestrieren.",
        )
        with gr.Tabs():
            build_welcome_tab()
            build_individual_agents_tab()
            build_mm_chat_tab()
            build_about_tab()
    return demo


demo = build_demo()


if __name__ == "__main__":
    demo.launch(
        server_name=config.GRADIO_SERVER_NAME,
        server_port=config.GRADIO_SERVER_PORT,
        theme=config.theme,
        css=config.GLOBAL_CSS,
    )
