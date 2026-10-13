"""Central runtime configuration for the SmolAgents workshop app.

Slim version of the parent template's config. Reads runtime settings from
the environment:

- ``GRADIO_SERVER_NAME`` (default ``"0.0.0.0"``)
- ``GRADIO_SERVER_PORT`` (default ``7860``)
- ``GENERATED_IMAGES_DIR`` (default ``runtime_data/generated_images``)
- ``OUTPUT_DIR`` (default ``runtime_data/output``)

The brand assets (``theme``, ``GLOBAL_CSS``) are computed at import time
from the bundled fonts and logo so the starter boots offline.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _env_str(key: str, default: str) -> str:
    raw = os.getenv(key)
    return raw if raw is not None and raw.strip() != "" else default


def _env_optional_str(key: str) -> str | None:
    raw = os.getenv(key)
    return raw if raw is not None and raw.strip() != "" else None


def _env_float(key: str, default: float) -> float:
    raw = os.getenv(key)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


STARTER_ROOT: Path = Path(__file__).resolve().parent

REPO_ROOT: Path = STARTER_ROOT

GRADIO_SERVER_NAME: str = _env_str("GRADIO_SERVER_NAME", "0.0.0.0")
GRADIO_SERVER_PORT: int = int(_env_str("GRADIO_SERVER_PORT", "7860") or "7860")


# ---------------------------------------------------------------------------
# ScaDS.AI API (OpenAI-compatible endpoint)
# ---------------------------------------------------------------------------
# Docs:     https://llm.scads.ai/
# API base: https://llm.scads.ai/v1
# API key:  TU Dresden self-service portal
#           https://selfservice.tu-dresden.de/services/scads-llm-api/
#
# Model aliases (stable across model rotations):
#   alias-vision             - vision-language model (default chat model)
#   alias-huge               - most powerful model
#   alias-code               - coding support
#   alias-reasoning          - reasoning tasks
#   alias-image-generation   - text-to-image (default image model)
#   alias-stt                - speech-to-text

SCADSAI_API_BASE: str = _env_str("SCADSAI_API_BASE", "https://llm.scads.ai/v1").rstrip("/")
SCADSAI_API_KEY: str | None = _env_optional_str("SCADSAI_API_KEY")
SCADSAI_CHAT_MODEL: str = _env_str("SCADSAI_CHAT_MODEL", "alias-vision")
SCADSAI_IMAGE_MODEL: str = _env_str("SCADSAI_IMAGE_MODEL", "alias-image-generation")
SCADSAI_REQUEST_TIMEOUT: float = _env_float("SCADSAI_REQUEST_TIMEOUT", 60.0)

# Where generated flyer images land on disk.
GENERATED_IMAGES_DIR: Path = Path(
    _env_str(
        "GENERATED_IMAGES_DIR",
        str(STARTER_ROOT / "runtime_data" / "generated_images"),
    )
).resolve()
GENERATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# geändert, OW:
# Workshop-Artefakte liegen bewusst unter runtime_data, damit generierte Dateien
# an einer Stelle gesammelt und per .gitignore ausgeschlossen werden. config.py
# legt den Ordner beim Start an; 
OUTPUT_DIR: Path = Path(_env_str("OUTPUT_DIR", str(STARTER_ROOT / "runtime_data" / "output"))).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Stronger model used by the orchestrator for routing and meta-questions.
SCADSAI_ORCHESTRATOR_MODEL: str = _env_str(
    "SCADSAI_ORCHESTRATOR_MODEL",
    "google/gemma-4-31B-it",
)


# ---------------------------------------------------------------------------
# Brand assets -- Living Lab theme + bundled Barlow / Open Sans webfonts.
# Copied from the parent template so the starter boots offline (no Google
# Fonts request at runtime).
# ---------------------------------------------------------------------------

# ``header.py`` is at <REPO>/gradio_ui/header.py. The logo lives in the
# sibling ``scads_ci/`` folder, and the fonts in ``fonts/``.
GRADIO_UI_DIR: Path = STARTER_ROOT / "gradio_ui"
FONTS_DIR: Path = GRADIO_UI_DIR / "fonts"
LOGO_PATH: Path = GRADIO_UI_DIR / "scads_ci" / "logo.png"


def _data_url(path: Path, mime: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _build_global_css() -> str:
    barlow_url = _data_url(FONTS_DIR / "Barlow-SemiBold.woff2", "font/woff2")
    opensans_url = _data_url(FONTS_DIR / "OpenSans-Regular.woff2", "font/woff2")
    return (
        "@font-face {"
        "  font-family: 'Barlow';"
        f"  src: url('{barlow_url}') format('woff2');"
        "  font-weight: 600;"
        "  font-style: normal;"
        "  font-display: swap;"
        "}"
        "@font-face {"
        "  font-family: 'Open Sans';"
        f"  src: url('{opensans_url}') format('woff2');"
        "  font-weight: 400 700;"
        "  font-style: normal;"
        "  font-display: swap;"
        "}"
        "html, body, .gradio-container, .prose, .md, textarea, input, button {"
        "  font-family: 'Open Sans', system-ui, sans-serif !important;"
        "}"
        "h1, h2, h3, h4, h5, h6 {"
        "  font-family: 'Barlow', system-ui, sans-serif !important;"
        "  font-weight: 600 !important;"
        "  letter-spacing: 0.01em;"
        "}"
    )


GLOBAL_CSS: str = _build_global_css()


# Theme re-export -- the brand contract (palette + button gradient) lives in
# ``gradio_ui/theme.py``. Import it here so ``app.py`` only needs to know
# about ``config``. The import is optional: if the Gradio version does not
# support themes (e.g. Gradio 6.x removed ``gr.themes``), ``theme`` falls
# back to ``None`` and the app uses the default Gradio theme.
try:
    from gradio_ui.theme import theme  # noqa: E402
except Exception:  # noqa: BLE001 -- theme is optional
    theme = None

__all__ = [
    "STARTER_ROOT",
    "REPO_ROOT",
    "GRADIO_SERVER_NAME",
    "GRADIO_SERVER_PORT",
    "SCADSAI_API_BASE",
    "SCADSAI_API_KEY",
    "SCADSAI_CHAT_MODEL",
    "SCADSAI_IMAGE_MODEL",
    "SCADSAI_REQUEST_TIMEOUT",
    "SCADSAI_ORCHESTRATOR_MODEL",
    "GENERATED_IMAGES_DIR",
    "OUTPUT_DIR",
    "GLOBAL_CSS",
    "theme",
]
