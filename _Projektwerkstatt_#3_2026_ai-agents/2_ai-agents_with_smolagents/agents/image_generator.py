"""Flyer-Generator Agent using SmolAgents.

This agent generates flyer images for arbitrary topics via the ScaDS.AI API.
It uses a ``ToolCallingAgent`` with five tools:

1. **enhance_flyer_prompt** -- Takes a vague topic (e.g. "AI in everyday life")
   and generates a detailed, visual prompt for a flyer background image.
   IMPORTANT: The prompt generates a background image WITHOUT text.

2. **generate_flyer_image** -- Calls the ScaDS.AI Image API
   (``alias-image-generation``) with the enhanced prompt, decodes the base64
   image and saves it under ``GENERATED_IMAGES_DIR``.

3. **generate_flyer_text** -- Calls the Chat-LLM and generates structured
   German flyer text (title, subtitle, body, call-to-action) as JSON.
   The LLM guarantees correct German spelling and grammar.

4. **overlay_flyer_text** -- Takes the generated background image and the
   structured text, renders the text onto the image with Pillow. Uses the
   corporate design fonts (Barlow SemiBold for titles, OpenSans Regular
   for body). Guarantees correct German text with umlauts (ä, ö, ü, ß).

5. **convert_flyer_to_pdf** -- Converts the generated flyer image into a
   PDF file using Pillow.

Two entry points:

* ``generate_flyer(topic)`` -- deterministic pipeline without the agent. Runs
  prompt enhancement, image generation, text generation and text overlay
  directly and returns a file path::

      from agents.image_generator import generate_flyer

      image_path = generate_flyer("KI im Alltag", size="1024x1792")

* ``create_agent()`` -- the agent that decides which tools to call in which
  order. The return value is the agent's answer (free text), not necessarily
  a path::

      agent = create_agent()
      answer = agent.run("Generate a flyer about AI in everyday life as PDF")
"""

from __future__ import annotations

import base64
import io
import json
import re
import textwrap
import threading
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import TypedDict

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from smolagents import OpenAIModel, ToolCallingAgent, tool

try:  # as package (agents.image_generator)
    from . import config
except ImportError:  # as flat module / script
    import config

# ---------------------------------------------------------------------------
# Constants & configuration
# ---------------------------------------------------------------------------

#: Allowed image sizes. The image API rejects anything else, so we validate
#: before the call -- otherwise the model invents values like "A4" or "800x600".
ALLOWED_SIZES: tuple[str, ...] = getattr(
    config,
    "SCADSAI_ALLOWED_IMAGE_SIZES",
    ("1024x1024", "1024x1792", "1792x1024"),
)
DEFAULT_SIZE: str = getattr(config, "SCADSAI_DEFAULT_IMAGE_SIZE", "1024x1792")

#: Prompt enhancement parameters.
ENHANCE_TEMPERATURE: float = getattr(config, "SCADSAI_ENHANCE_TEMPERATURE", 0.7)
ENHANCE_MAX_TOKENS: int = getattr(config, "SCADSAI_ENHANCE_MAX_TOKENS", 512)

#: Text generation parameters.
TEXT_TEMPERATURE: float = getattr(config, "SCADSAI_TEXT_TEMPERATURE", 0.7)
TEXT_MAX_TOKENS: int = getattr(config, "SCADSAI_TEXT_MAX_TOKENS", 512)

#: DPI for PDF export. Without this value Pillow assumes 72 dpi, a 1024-px
#: image would then be embedded as a ~36 cm wide page.
PDF_RESOLUTION: float = getattr(config, "PDF_RESOLUTION", 300.0)

_SIZE_RE = re.compile(r"^\d{3,4}x\d{3,4}$")

#: Magic bytes -> file extension. The API delivers PNG or JPEG depending on
#: the model; appending ".jpg" wholesale creates files with the wrong extension.
_MAGIC_BYTES: tuple[tuple[bytes, str], ...] = (
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpg"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
)

#: Overlay colours (Living Lab palette, design_spec.md §2.1).
#: Dark blue with transparency for the text block background overlay.
OVERLAY_BG_TOP = (0, 75, 111, 200)  # dark-blue, ~78% opacity
OVERLAY_BG_BOTTOM = (0, 75, 111, 200)  # dark-blue, ~78% opacity
OVERLAY_TEXT_COLOR = (255, 255, 255)  # white -- safe contrast (§6)

#: Relative sizes for the text overlay, scaled to image width.
#: These values were calibrated for 1024-px width.
TITLE_FONT_RATIO = 0.055  # ~56 px at 1024 px
SUBTITLE_FONT_RATIO = 0.032  # ~33 px at 1024 px
BODY_FONT_RATIO = 0.024  # ~25 px at 1024 px
CTA_FONT_RATIO = 0.035  # ~36 px at 1024 px
OVERLAY_TOP_RATIO = 0.32  # upper overlay area: 32% of height
OVERLAY_BOTTOM_RATIO = 0.28  # lower overlay area: 28% of height
OVERLAY_PADDING_RATIO = 0.04  # inner padding: 4% of width


# ---------------------------------------------------------------------------
# TypedDict for structured flyer text
# ---------------------------------------------------------------------------


class FlyerText(TypedDict):
    """Structured flyer text in correct German."""

    title: str
    subtitle: str
    body: str
    call_to_action: str


# ---------------------------------------------------------------------------
# Client management (cached OpenAI client for ScaDS.AI API calls)
# ---------------------------------------------------------------------------

_client: OpenAI | None = None
_client_lock = threading.Lock()


def _require_api_key() -> str:
    """Return the configured API key or raise a helpful error."""
    key = config.SCADSAI_API_KEY
    if not key:
        raise RuntimeError(
            "SCADSAI_API_KEY is not set. Copy .env.example to .env and fill in SCADSAI_API_KEY=..."
        )
    return key


def _get_client() -> OpenAI:
    """Return a cached ``OpenAI`` client pointed at the ScaDS.AI endpoint.

    Raises ``RuntimeError`` if ``SCADSAI_API_KEY`` is not set.
    """
    global _client
    if _client is None:
        with _client_lock:
            if _client is None:
                _client = OpenAI(
                    base_url=config.SCADSAI_API_BASE,
                    api_key=_require_api_key(),
                    timeout=config.SCADSAI_REQUEST_TIMEOUT,
                )
    return _client


def _images_dir() -> Path:
    """Return the output directory, creating it if necessary."""
    target = Path(config.GENERATED_IMAGES_DIR)
    target.mkdir(parents=True, exist_ok=True)
    return target


def _detect_extension(data: bytes, default: str = "png") -> str:
    """Guess the image file extension from its magic bytes."""
    for magic, ext in _MAGIC_BYTES:
        if data.startswith(magic):
            return ext
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return default


def _safe_filename(prompt: str, ext: str) -> str:
    """Generate a collision-free, filesystem-safe filename from a prompt."""
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", prompt.strip()).strip("-")[:40] or "flyer"
    return f"{slug}-{uuid.uuid4().hex[:8]}.{ext}"


def _validate_size(size: str | None) -> str:
    """Normalise and validate a "WIDTHxHEIGHT" size string."""
    if not size:
        return DEFAULT_SIZE
    normalised = size.strip().lower().replace("×", "x").replace(" ", "")
    if normalised not in ALLOWED_SIZES:
        if not _SIZE_RE.match(normalised):
            raise ValueError(f"Invalid size {size!r}. Use one of: {', '.join(ALLOWED_SIZES)}.")
        raise ValueError(
            f"Size {normalised!r} is not supported by the image API. "
            f"Use one of: {', '.join(ALLOWED_SIZES)}."
        )
    return normalised


def _resolve_generated_file(image_path: str) -> Path:
    """Resolve a path and ensure it points at a file inside the images dir.

    The agent controls this argument, so we do not want it reading arbitrary
    files from disk.
    """
    base = _images_dir().resolve()
    candidate = Path(image_path).expanduser().resolve()

    if not candidate.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if base not in candidate.parents:
        raise ValueError(
            f"Refusing to read {image_path!r}: only files inside {base} may be converted."
        )
    return candidate


# ---------------------------------------------------------------------------
# Font loading (woff2 -> ttf via fonttools, fallback DejaVu)
# ---------------------------------------------------------------------------

#: Corporate design fonts (woff2). Converted to TTF at runtime so Pillow can
#: load them with ``ImageFont.truetype()``.
_FONT_HEADLINE_PATH = Path(config.STARTER_ROOT) / "gradio_ui" / "fonts" / "Barlow-SemiBold.woff2"
_FONT_BODY_PATH = Path(config.STARTER_ROOT) / "gradio_ui" / "fonts" / "OpenSans-Regular.woff2"

#: System font fallbacks. DejaVu Sans is always present on Linux and has
#: excellent Unicode support including German umlauts.
_SYSTEM_FONT_CANDIDATES: tuple[str, ...] = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf",
)

_FONT_CACHE: dict[str, ImageFont.FreeTypeFont] = {}


def _woff2_to_ttf_buffer(woff2_path: Path) -> io.BytesIO:
    """Convert a .woff2 font to an in-memory TTF buffer via fonttools."""
    from fontTools.ttLib import TTFont

    font = TTFont(woff2_path)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    return buf


def _find_system_font() -> str:
    """Return the first available system font path, or empty string."""
    for candidate in _SYSTEM_FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return ""


def _load_font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a font with fallback chain.

    Parameters
    ----------
    kind
        ``"headline"`` (Barlow SemiBold) or ``"body"`` (OpenSans Regular).
    size
        Font size in pixels.

    Fallback order:
    1. Corporate design font (woff2 -> ttf via fonttools)
    2. System font (DejaVu Sans / Ubuntu Sans)
    3. Pillow default font (not proportional, but works)
    """
    cache_key = f"{kind}:{size}"
    if cache_key in _FONT_CACHE:
        return _FONT_CACHE[cache_key]

    woff2_path = _FONT_HEADLINE_PATH if kind == "headline" else _FONT_BODY_PATH
    font: ImageFont.FreeTypeFont | None = None

    # 1st attempt: corporate design font (woff2)
    if woff2_path.exists():
        try:
            ttf_buf = _woff2_to_ttf_buffer(woff2_path)
            font = ImageFont.truetype(ttf_buf, size)
        except Exception:  # noqa: BLE001 -- fallback follows
            font = None

    # 2nd attempt: system font
    if font is None:
        sys_path = _find_system_font()
        if sys_path:
            try:
                font = ImageFont.truetype(sys_path, size)
            except Exception:  # noqa: BLE001 -- fallback follows
                font = None

    # 3rd attempt: Pillow default
    if font is None:
        font = ImageFont.load_default()

    _FONT_CACHE[cache_key] = font
    return font


# ---------------------------------------------------------------------------
# Prompt enhancement -- background image WITHOUT text
# ---------------------------------------------------------------------------


def enhance_prompt(topic: str) -> str:
    """Turn a vague topic into a detailed image prompt for a flyer background.

    IMPORTANT: The prompt generates a background image **without text**. The
    text is rendered separately with Pillow later (see ``render_flyer_text``).
    This prevents hallucinated/garbled text in the generated image.

    Args:
        topic: A short description of the flyer's theme (e.g., "KI im Alltag").

    Returns:
        A detailed image generation prompt as a string.
    """
    if not topic or not topic.strip():
        raise ValueError("topic must not be empty.")

    client = _get_client()

    system_prompt = (
        "Du bist ein Experte für Flyer-Design und visuelle Kommunikation. "
        "Deine Aufgabe ist es, ein vages Thema in einen detaillierten, "
        "bildhaften Prompt für einen Flyer-Hintergrund zu verwandeln.\n\n"
        "ABSOLUTE REGEL: Das Bild darf KEINEN Text enthalten – weder "
        "Buchstaben, Wörter, Sätze noch einzelne Glyphen. Der Text wird "
        "später separat mit Pillow auf das Bild gerendert.\n\n"
        "Der Prompt soll enthalten:\n"
        "- Visuelle Beschreibung (Komposition, Perspektive)\n"
        "- Farbpalette (konkret, z.B. 'dunkelblau, grün, weiß')\n"
        "- Stimmung und Atmosphäre\n"
        "- Klare leere Bereiche für Text-Overlay (z.B. 'large empty space "
        "at the top for title text', 'empty space at the bottom for body "
        "text')\n"
        "- Stil (z.B. 'flat design', 'illustrativ', 'fotorealistisch')\n\n"
        "WICHTIG: Antworte NUR mit dem enhanced Prompt, ohne Erklärungen. "
        "Der Prompt soll auf Englisch sein und ein einzelner Absatz sein."
    )

    try:
        response = client.chat.completions.create(
            model=config.SCADSAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Thema: {topic}"},
            ],
            temperature=ENHANCE_TEMPERATURE,
            max_tokens=ENHANCE_MAX_TOKENS,
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Prompt enhancement failed: {exc}") from exc

    enhanced = (response.choices[0].message.content or "").strip()
    if not enhanced:
        raise RuntimeError("Prompt enhancement returned empty result.")

    return enhanced


# ---------------------------------------------------------------------------
# Flyer text generation -- structured German text via LLM
# ---------------------------------------------------------------------------


def create_flyer_text(topic: str) -> str:
    """Generate structured German flyer text via the Chat-LLM.

    The LLM generates a JSON object with four fields:
    ``title``, ``subtitle``, ``body``, ``call_to_action``.

    The system prompt emphasises:
    - Correct German spelling and grammar
    - Correct umlauts (ä, ö, ü) and ß
    - Short and concise (for a flyer)

    Args:
        topic: A short description of the flyer's theme.

    Returns:
        A JSON string with the flyer text fields.
    """
    if not topic or not topic.strip():
        raise ValueError("topic must not be empty.")

    client = _get_client()

    system_prompt = (
        "Du bist ein Experte für Flyer-Texte in korrekter deutscher Sprache.\n"
        "Deine Aufgabe ist es, ansprechende Flyer-Texte zu einem gegebenen "
        "Thema zu generieren.\n\n"
        "ABSOLUTE REGELN:\n"
        "- Verwende korrekte deutsche Rechtschreibung und Grammatik.\n"
        "- Verwende korrekte Umlaute (ä, ö, ü) und ß.\n"
        "- Halte die Texte kurz und prägnant – passend für einen Flyer.\n"
        "- Der Titel soll max. 6 Wörter sein.\n"
        "- Der Untertitel soll max. 12 Wörter sein.\n"
        "- Der Body-Text soll max. 30 Wörter sein.\n"
        "- Der Call-to-Action soll max. 8 Wörter sein.\n\n"
        "Antworte NUR mit einem JSON-Objekt in genau diesem Format:\n"
        '{"title": "...", "subtitle": "...", "body": "...", '
        '"call_to_action": "..."}\n'
        "Keine Erklärungen, kein Markdown, nur das JSON-Objekt."
    )

    try:
        response = client.chat.completions.create(
            model=config.SCADSAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Thema: {topic}"},
            ],
            temperature=TEXT_TEMPERATURE,
            max_tokens=TEXT_MAX_TOKENS,
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Flyer text generation failed: {exc}") from exc

    raw = (response.choices[0].message.content or "").strip()
    if not raw:
        raise RuntimeError("Flyer text generation returned empty result.")

    text_data = _parse_flyer_text_json(raw)
    return json.dumps(text_data, ensure_ascii=False)


def _parse_flyer_text_json(raw: str) -> FlyerText:
    """Parse and validate the JSON returned by the LLM.

    Handles common LLM quirks: surrounding markdown fences, extra text
    before/after the JSON object, and nested or malformed braces.
    """
    # 1st attempt: direct JSON parsing
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # 2nd attempt: extract JSON from markdown code block
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Failed to parse flyer text JSON from markdown: {exc}") from exc
        else:
            # 3rd attempt: extract first {...} construct
            match = re.search(r"\{.*?\}", raw, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError as exc:
                    raise RuntimeError(
                        f"Failed to parse flyer text JSON: {exc}\nRaw: {raw}"
                    ) from exc
            else:
                raise RuntimeError(f"No JSON object found in LLM response.\nRaw: {raw}") from None

    # Validate fields
    required = ["title", "subtitle", "body", "call_to_action"]
    for field in required:
        if field not in data:
            raise RuntimeError(f"Flyer text JSON missing field: {field}")
        if not isinstance(data[field], str) or not data[field].strip():
            raise RuntimeError(f"Flyer text field '{field}' is empty or not a string.")

    return data  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------


def generate_image(prompt: str, size: str | None = None) -> str:
    """Generate an image and return its path. See tool wrapper."""
    if not prompt or not prompt.strip():
        raise ValueError("prompt must not be empty.")

    validated_size = _validate_size(size)
    client = _get_client()

    try:
        response = client.images.generate(
            model=config.SCADSAI_IMAGE_MODEL,
            prompt=prompt,
            n=1,
            size=validated_size,
            response_format="b64_json",
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Image generation failed: {exc}") from exc

    if not response.data:
        raise RuntimeError("Image API returned no data.")

    item = response.data[0]
    b64 = getattr(item, "b64_json", None)
    url = getattr(item, "url", None)

    if b64:
        data = base64.b64decode(b64)
    elif url:
        data = _download(url)
    else:
        raise RuntimeError("Image API returned neither b64_json nor url.")

    if not data:
        raise RuntimeError("Image API returned an empty image.")

    target = _images_dir() / _safe_filename(prompt, _detect_extension(data))
    target.write_bytes(data)
    return str(target)


def _download(url: str) -> bytes:
    """Fetch image bytes from an http(s) URL returned by the API."""
    scheme = urllib.parse.urlparse(url).scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"Refusing to fetch image from non-HTTP URL: {url!r}")
    with urllib.request.urlopen(url, timeout=config.SCADSAI_REQUEST_TIMEOUT) as r:
        return r.read()


# ---------------------------------------------------------------------------
# Text overlay -- render text onto image with Pillow
# ---------------------------------------------------------------------------


def render_flyer_text(image_path: str, flyer_text_json: str) -> str:
    """Overlay structured German text on a flyer image using Pillow.

    Renders title, subtitle, body, and call-to-action text on the image
    using corporate design fonts (Barlow SemiBold for headlines, OpenSans
    Regular for body text). Uses semi-transparent dark-blue overlay bands
    at the top and bottom of the image to ensure WCAG-compliant contrast
    (white text on dark-blue, >= 4.5:1 per design_spec.md §6).

    Args:
        image_path: The local file path to the background image (as returned
            by ``generate_flyer_image``).
        flyer_text_json: A JSON string with keys ``title``, ``subtitle``,
            ``body``, ``call_to_action`` (as returned by
            ``generate_flyer_text``).

    Returns:
        The local file path to the final flyer image with text overlay.
    """
    # Parse and validate flyer text JSON
    try:
        text_data: FlyerText = json.loads(flyer_text_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid flyer text JSON: {exc}") from exc

    required = ["title", "subtitle", "body", "call_to_action"]
    for field in required:
        if field not in text_data or not text_data[field]:
            raise ValueError(f"Flyer text missing required field: {field}")

    # Load image
    src = _resolve_generated_file(image_path)
    img = Image.open(src).convert("RGBA")
    width, height = img.size

    # Create overlay
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Calculate layout
    padding = int(width * OVERLAY_PADDING_RATIO)
    top_band_h = int(height * OVERLAY_TOP_RATIO)
    bottom_band_h = int(height * OVERLAY_BOTTOM_RATIO)

    # Calculate font sizes
    title_size = max(16, int(width * TITLE_FONT_RATIO))
    subtitle_size = max(12, int(width * SUBTITLE_FONT_RATIO))
    body_size = max(10, int(width * BODY_FONT_RATIO))
    cta_size = max(14, int(width * CTA_FONT_RATIO))

    # Load fonts
    title_font = _load_font("headline", title_size)
    subtitle_font = _load_font("body", subtitle_size)
    body_font = _load_font("body", body_size)
    cta_font = _load_font("headline", cta_size)

    # --- Top overlay: title + subtitle ---
    draw.rectangle([0, 0, width, top_band_h], fill=OVERLAY_BG_TOP)

    _draw_centered_text(
        draw,
        text_data["title"],
        title_font,
        width,
        y_start=padding,
        y_end=top_band_h // 2,
        color=OVERLAY_TEXT_COLOR,
    )
    _draw_centered_text(
        draw,
        textwrap.fill(text_data["subtitle"], width=55),
        subtitle_font,
        width,
        y_start=top_band_h // 2,
        y_end=top_band_h - padding // 2,
        color=OVERLAY_TEXT_COLOR,
    )

    # --- Bottom overlay: body + call-to-action ---
    bottom_y = height - bottom_band_h
    draw.rectangle([0, bottom_y, width, height], fill=OVERLAY_BG_BOTTOM)

    body_y_start = bottom_y + padding
    body_y_end = bottom_y + bottom_band_h - cta_size - padding
    _draw_wrapped_text(
        draw,
        text_data["body"],
        body_font,
        width,
        y_start=body_y_start,
        y_end=body_y_end,
        color=OVERLAY_TEXT_COLOR,
        padding=padding,
    )

    _draw_centered_text(
        draw,
        text_data["call_to_action"],
        cta_font,
        width,
        y_start=height - cta_size - padding,
        y_end=height - padding // 2,
        color=OVERLAY_TEXT_COLOR,
    )

    # Composite overlay onto original image
    result = Image.alpha_composite(img, overlay)
    result_rgb = result.convert("RGB")

    # Save
    target = _images_dir() / _safe_filename("flyer_with_text", "png")
    result_rgb.save(target, "PNG")
    result_rgb.close()
    img.close()

    return str(target)


def _draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    image_width: int,
    y_start: int,
    y_end: int,
    color: tuple[int, int, int, int],
) -> None:
    """Draw text horizontally centered within a vertical band."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    if text_w > image_width - 20:
        text_w = image_width - 20

    x = (image_width - text_w) // 2
    y = y_start + (y_end - y_start - text_h) // 2

    draw.text((x, y), text, font=font, fill=color)


def _draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    image_width: int,
    y_start: int,
    y_end: int,
    color: tuple[int, int, int, int],
    padding: int,
) -> None:
    """Draw left-aligned text with word wrapping within a vertical band."""
    max_width = image_width - 2 * padding
    if max_width <= 0:
        max_width = image_width

    avg_char_w = font.size * 0.55
    chars_per_line = max(10, int(max_width / avg_char_w))

    lines = textwrap.wrap(text, width=chars_per_line)
    if not lines:
        lines = [text]

    line_h = int(font.size * 1.4)
    y = y_start

    for line in lines:
        if y + line_h > y_end:
            break
        draw.text((padding, y), line, font=font, fill=color)
        y += line_h


# ---------------------------------------------------------------------------
# PDF conversion
# ---------------------------------------------------------------------------


def convert_to_pdf(image_path: str) -> str:
    """Convert a generated image to a single-page PDF. See tool wrapper."""
    src = _resolve_generated_file(image_path)
    pdf_path = _images_dir() / f"{src.stem}.pdf"

    with Image.open(src) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(pdf_path, "PDF", resolution=PDF_RESOLUTION)

    return str(pdf_path)


# ---------------------------------------------------------------------------
# Tool wrappers (for the SmolAgents agent)
# ---------------------------------------------------------------------------


@tool
def enhance_flyer_prompt(topic: str) -> str:
    """Enhance a vague topic into a detailed image prompt for a flyer background.

    The prompt generates a background image WITHOUT any text. Text is added
    separately later via overlay_flyer_text. This prevents garbled/hallucinated
    text in the generated image.

    Args:
        topic: A short description of the flyer's theme (e.g., "KI im Alltag").

    Returns:
        A detailed image generation prompt as a string.
    """
    return enhance_prompt(topic)


@tool
def generate_flyer_image(prompt: str, size: str) -> str:
    """Generate a flyer background image from a detailed prompt.

    This tool calls the image generation API (alias-image-generation) with the
    given prompt and saves the result as an image file. The image will NOT
    contain text -- text is overlaid separately.

    Args:
        prompt: A detailed image generation prompt (ideally enhanced via
            enhance_flyer_prompt first).
        size: The image size, one of "1024x1024" (square), "1024x1792"
            (portrait) or "1792x1024" (landscape). Portrait is recommended
            for flyers.

    Returns:
        The local file path to the generated background image.
    """
    return generate_image(prompt, size)


@tool
def generate_flyer_text(topic: str) -> str:
    """Generate structured German flyer text via the Chat-LLM.

    The LLM generates correct German text with proper umlauts (ä, ö, ü) and ß
    structured as JSON with four fields:
    - title: Short, catchy title (max 6 words)
    - subtitle: Descriptive subtitle (max 12 words)
    - body: Main body text (max 30 words)
    - call_to_action: Call-to-action (max 8 words)

    Args:
        topic: A short description of the flyer's theme.

    Returns:
        A JSON string with the flyer text fields.
    """
    return create_flyer_text(topic)


@tool
def overlay_flyer_text(image_path: str, flyer_text_json: str) -> str:
    """Overlay structured German text on a flyer image using Pillow.

    This tool takes a background image (from generate_flyer_image) and
    overlays German text (from generate_flyer_text) on it. The text is
    rendered with Pillow using corporate design fonts (Barlow SemiBold
    for headlines, OpenSans Regular for body), guaranteeing correct
    German text with proper umlauts.

    The overlay uses semi-transparent dark-blue bands at the top and bottom
    of the image, with white text, ensuring WCAG-compliant contrast.

    Args:
        image_path: The local file path to the background image (as returned
            by generate_flyer_image).
        flyer_text_json: A JSON string with keys "title", "subtitle", "body",
            "call_to_action" (as returned by generate_flyer_text).

    Returns:
        The local file path to the final flyer image with text overlay.
    """
    return render_flyer_text(image_path, flyer_text_json)


@tool
def convert_flyer_to_pdf(image_path: str) -> str:
    """Convert a generated flyer image to PDF format.

    This tool takes the file path of a generated flyer image (JPEG/PNG)
    and converts it to a single-page PDF file using Pillow.

    Args:
        image_path: The local file path to the flyer image (as returned by
            generate_flyer_image or overlay_flyer_text).

    Returns:
        The local file path to the generated PDF file.
    """
    return convert_to_pdf(image_path)


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------


def create_agent() -> ToolCallingAgent:
    """Create and return a configured Flyer-Generator Agent.

    The agent uses the ScaDS.AI chat model for reasoning and tool selection.
    It has access to five tools:

    1. ``enhance_flyer_prompt`` -- enhances a topic into a background image prompt
    2. ``generate_flyer_image`` -- generates the background image (no text)
    3. ``generate_flyer_text`` -- generates structured German text (JSON)
    4. ``overlay_flyer_text`` -- overlays the text on the image with Pillow
    5. ``convert_flyer_to_pdf`` -- converts the final flyer to PDF

    Returns:
        A configured ``ToolCallingAgent`` instance.

    Raises:
        RuntimeError: If ``SCADSAI_API_KEY`` is not set.
    """
    model = OpenAIModel(
        model_id=config.SCADSAI_CHAT_MODEL,
        api_base=config.SCADSAI_API_BASE,
        api_key=_require_api_key(),
    )
    # geändert, OW:
    # Kein globales tool_choice am Model setzen. Der Agent hat zwar Tools, aber
    # nicht jeder LLM-Request enthält ein tools-Payload; SmolAgents soll diese
    # Details pro Schritt selbst setzen.

    return ToolCallingAgent(
        tools=[
            enhance_flyer_prompt,
            generate_flyer_image,
            generate_flyer_text,
            overlay_flyer_text,
            convert_flyer_to_pdf,
        ],
        model=model,
        name="flyer_generator",
        description=(
            "An agent that generates flyer images for arbitrary topics. "
            "The agent can: (1) enhance a topic into a detailed image prompt, "
            "(2) generate a flyer background image (without text), (3) generate "
            "structured German flyer text, (4) overlay the text onto the image "
            "with Pillow, and (5) export the final flyer as PDF."
        ),
        instructions=(
            "You are a flyer-generator agent. Your task is to generate flyer "
            "images for arbitrary topics.\n\n"
            "Typical workflow:\n"
            "1. enhance_flyer_prompt: Takes a topic and generates a detailed "
            "image prompt for the background image (without text).\n"
            "2. generate_flyer_image: Generates the flyer background image from "
            "the enhanced prompt. Default size is 1024x1792 (portrait).\n"
            "3. generate_flyer_text: Generates structured German flyer text "
            "(title, subtitle, body, call-to-action) as JSON.\n"
            "4. overlay_flyer_text: Renders the German text onto the background "
            "image with Pillow. This guarantees correct German text.\n"
            "5. convert_flyer_to_pdf: Converts the finished flyer image into a "
            "PDF file.\n\n"
            "IMPORTANT: The text is NOT rendered by the image generation model. "
            "It is rendered separately with Pillow. This guarantees correct "
            "German text with umlauts (ä, ö, ü) and ß.\n\n"
            "When the user asks for a flyer, execute steps 1-4. When the user "
            "explicitly asks for a PDF, also execute step 5. Always return the "
            "file path of the result at the end."
        ),
        max_steps=15,
    )


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------


def generate_flyer(
    topic: str,
    size: str = DEFAULT_SIZE,
    as_pdf: bool = False,
) -> str:
    """Generate a flyer for the given topic -- deterministic, without the agent.

    Runs the full pipeline directly:

    1. ``enhance_prompt(topic)`` -- generate background image prompt
    2. ``generate_image(prompt, size)`` -- generate background image
    3. ``create_flyer_text(topic)`` -- generate structured German text
    4. ``render_flyer_text(image_path, flyer_text_json)`` -- overlay text
    5. ``convert_to_pdf(image_path)`` -- convert to PDF (if ``as_pdf``)

    Args:
        topic: A short description of the flyer's theme.
        size: The image size, one of ``ALLOWED_SIZES`` (default portrait).
        as_pdf: If True, also convert the image and return the PDF path.

    Returns:
        The local file path to the generated flyer image, or to the PDF if
        ``as_pdf`` is True.
    """
    prompt = enhance_prompt(topic)
    image_path = generate_image(prompt, size)
    flyer_text_json = create_flyer_text(topic)
    final_image_path = render_flyer_text(image_path, flyer_text_json)
    return convert_to_pdf(final_image_path) if as_pdf else final_image_path


def run_flyer_agent(request: str) -> str:
    """Run the agent on a free-text request and return its final answer.

    Unlike :func:`generate_flyer` the result is whatever the agent decides to
    answer -- usually, but not guaranteed to be, a file path.
    """
    return str(create_agent().run(request))


__all__ = [
    "ALLOWED_SIZES",
    "DEFAULT_SIZE",
    "FlyerText",
    "enhance_prompt",
    "create_flyer_text",
    "generate_image",
    "render_flyer_text",
    "convert_to_pdf",
    "enhance_flyer_prompt",
    "generate_flyer_image",
    "generate_flyer_text",
    "overlay_flyer_text",
    "convert_flyer_to_pdf",
    "create_agent",
    "generate_flyer",
    "run_flyer_agent",
]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Flyer-Generator")
    parser.add_argument("topic", help="Thema des Flyers, z.B. 'KI im Alltag'")
    parser.add_argument("--size", default=DEFAULT_SIZE, choices=list(ALLOWED_SIZES))
    parser.add_argument("--pdf", action="store_true", help="zusätzlich als PDF")
    parser.add_argument(
        "--agent",
        action="store_true",
        help="über den Agenten statt der direkten Pipeline laufen lassen",
    )
    args = parser.parse_args()

    if args.agent:
        suffix = " Exportiere das Ergebnis als PDF." if args.pdf else ""
        print(run_flyer_agent(f"Generiere einen Flyer zum Thema: {args.topic}.{suffix}"))
    else:
        print(generate_flyer(args.topic, size=args.size, as_pdf=args.pdf))
