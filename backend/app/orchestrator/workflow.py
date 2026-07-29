"""Workflow enumerations and definitions for Multi-Agent Orchestrator."""

from enum import StrEnum


class WorkflowStatus(StrEnum):
    """Lifecycle execution status of a multi-agent workflow."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStep(StrEnum):
    """Identifies individual execution steps in multi-agent workflow."""

    PLANNING = "planning"
    RESEARCHING = "researching"
    WRITING = "writing"
    REVIEWING = "reviewing"
