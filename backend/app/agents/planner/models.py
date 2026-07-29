"""Domain models for Planner Agent."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskModel:
    """Represents an individual task in a research plan."""

    id: str
    title: str
    description: str
    priority: str = "medium"
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert task model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "reason": self.reason,
        }


@dataclass
class PlannerResult:
    """Structured plan output produced by the Planner Agent."""

    goal: str
    summary: str
    tasks: list[TaskModel] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    expected_output: str = ""
    estimated_steps: int = 1
    estimated_complexity: str = "medium"
    clarification_required: bool = False
    clarification_questions: list[str] = field(default_factory=list)
