"""Global page header — ScaDS.AI logo + gradient title.

This module is one of two brand-contract files you should **reuse, not
re-implement** when deriving a new demo from the template (the other is
``gradio_ui/theme.py``). Both together implement the Living Lab look
defined in ``design_spec.md``.

Webfonts (Barlow, Open Sans) and the brand palette come from
``config.GLOBAL_CSS`` and are injected via the ``css=`` parameter on
``launch()``. This file only handles the header layout (logo + gradient
title) which is element-specific.
"""

from __future__ import annotations

import base64
from pathlib import Path

import gradio as gr

_HEADER_STYLE = """
#scads-header {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
#scads-logo {
    height: 60px;
    width: auto;
}
#scads-header-text h1 {
    margin: 0;
    background: linear-gradient(90deg, #0074ac 0%, #71BD56 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    line-height: 1.2;
}
#scads-header-text p {
    margin: 0.25rem 0 0 0;
    color: #444;
    font-size: 1.1rem;
}
@media (max-width: 768px) {
    #scads-header {
        flex-direction: column;
        text-align: center;
    }
    #scads-logo {
        margin-bottom: 1rem;
    }
    #scads-header-text h1 {
        font-size: 2rem;
    }
}
"""


def render_global_header(
    title: str = "ScaDS.AI Living Lab Demonstrator",
    tagline: str = "Local multimodal chat powered by an open-source LLM",
) -> None:
    """Inject the header once at the top of the top-level ``gr.Blocks``.

    Parameters
    ----------
    title:
        The main headline. Keep it concise (one line at desktop widths).
    tagline:
        A single-sentence subtitle. Used as the visual lead-in under the
        title; carries no semantic role beyond decoration.
    """
    logo_path = Path(__file__).parent / "scads_ci" / "logo.png"
    logo_base64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    logo_src = f"data:image/png;base64,{logo_base64}"

    gr.HTML(
        f"""
        <style>{_HEADER_STYLE}</style>
        <div id="scads-header">
            <img id="scads-logo" src="{logo_src}" alt="ScaDS.AI Logo">
            <div id="scads-header-text">
                <h1>{title}</h1>
                <p>{tagline}</p>
            </div>
        </div>
        """
    )
