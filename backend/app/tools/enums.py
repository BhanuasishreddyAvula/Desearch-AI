"""Enumerations for Tool Registry domain."""

from enum import StrEnum


class ToolCategory(StrEnum):
    """Categories classifying tool capabilities."""

    SEARCH = "search"
    FETCH = "fetch"
    DOCUMENT = "document"
    CITATION = "citation"
    UTILITY = "utility"


class AgentType(StrEnum):
    """AI agent role types that can utilize tools."""

    PLANNER = "planner"
    RESEARCH = "research"
    WRITER = "writer"
    REVIEWER = "reviewer"
    ORCHESTRATOR = "orchestrator"
