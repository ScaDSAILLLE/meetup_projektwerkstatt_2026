"""Agents package -- Multi-Agent-System für das ScaDS.AI Living Lab.

Verfügbare Agenten:

- ``agents.image_generator`` -- Flyer-Generator Agent
- ``agents.agent_workshop`` -- Workshop-Generator Agent
- ``agents.orchestrator`` -- Orchestrator Agent (verwaltet Sub-Agenten)

Einstiegspunkt für die UI:

    from agents import create_orchestrator

    orchestrator = create_orchestrator()
    response = orchestrator.run("Welche Aufgaben kannst du?")
"""

from agents.agent_workshop import create_agent as create_workshop_agent
from agents.image_generator import create_agent as create_flyer_agent
from agents.orchestrator import create_orchestrator

__all__ = [
    "create_orchestrator",
    "create_workshop_agent",
    "create_flyer_agent",
]
