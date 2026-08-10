"""About tab for the SmolAgents Projektwerkstatt app."""

from __future__ import annotations

import gradio as gr

ABOUT_TEXT = """
## About

Diese Demo wurde für eine ScaDS.AI Living Lab Projektwerkstatt gebaut. Sie soll zeigen, wie schnell sich mit Hugging Face `smolagents` ein kleines Multi-Agentensystem aufbauen lässt.

### Was zeigt die Demo?

Die App zeigt zwei Ebenen:

- Einzelne Spezial-Agenten, die direkt getestet werden können.
- Einen Orchestrator-Agenten, der Aufgaben an diese Spezial-Agenten delegiert.

Damit wird sichtbar, was ein Agent ist, was ein Tool ist und wie aus mehreren Agenten ein koordiniertes System entsteht.

### Wie funktioniert sie?

Die Gradio-App ruft SmolAgents-Agenten im Python-Prozess auf. Jeder Agent nutzt ein OpenAI-kompatibles Modell über die ScaDS.AI API. Die Agenten bekommen Werkzeuge als Python-Funktionen, zum Beispiel zum Schreiben von Dateien, Erstellen von Präsentationen oder Generieren von Bildern.

Der Orchestrator ist selbst ein `ToolCallingAgent`. Er bekommt die Spezial-Agenten als `managed_agents` und entscheidet, an wen er eine Aufgabe delegiert.

### Wofür ist das nützlich?

Agenten eignen sich gut, wenn ein Sprachmodell nicht nur antworten, sondern gezielt Schritte ausführen soll: Tools wählen, Ergebnisse prüfen, Dateien erzeugen oder mehrere Teilaufgaben koordinieren. Das Beispiel ist bewusst klein gehalten, damit es im Workshop verstanden und erweitert werden kann.

### Grenzen

- Die Qualität hängt vom verwendeten Modell und den Agenten-Instruktionen ab.
- Generierte Dateien sollten geprüft werden.
- Tools brauchen klare Grenzen, besonders wenn sie Dateien lesen, schreiben oder externe Dienste nutzen.
- Ein Orchestrator macht ein System flexibler, aber auch weniger direkt vorhersagbar als ein einzelner Funktionsaufruf.

### Credits und Links

Diese Demo nutzt das ScaDS.AI Living Lab Gradio-Template, die ScaDS.AI API, Gradio, Pillow, python-pptx und Hugging Face SmolAgents.

- [ScaDS.AI Dresden/Leipzig](https://scads.ai/)
- [ScaDS.AI Living Lab](https://scads.ai/living-lab/)
- [Hugging Face SmolAgents](https://huggingface.co/docs/smolagents/index)
- [Gradio](https://www.gradio.app/)

Danke an alle Demo-Macherinnen und Demo-Macher, die Projektwerkstatt-Materialien, OpenCode-Setups und Living-Lab-Templates vorbereitet und weiterentwickelt haben.
"""


def build_about_tab() -> None:
    with gr.Tab("About"):
        gr.Markdown(ABOUT_TEXT)
