"""Pydantic v2 schemas for Planner Agent API requests and responses."""

from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class PlanRequest(BaseModel):
    """Request payload for generating a research plan."""

    session_id: str = Field(
        ..., description="UUID identifier of the ResearchSession in Supabase"
    )


class TaskSchema(BaseModel):
    """Schema representing a single research plan task."""

    id: str = Field(..., description="Unique task identifier, e.g., task_1")
    title: str = Field(..., description="Short descriptive title of the task")
    description: str = Field(
        ..., description="Detailed instructions for the research task"
    )
    priority: str = Field(
        default="medium", description="Task priority (high, medium, low)"
    )
    reason: str = Field(
        default="", description="Justification for including this task"
    )


class PlannerResultSchema(BaseModel):
    """Pydantic representation of PlannerResult for API serialization."""

    goal: str = Field(..., description="Deconstructed primary research goal")
    summary: str = Field(
        ..., description="Executive summary of proposed research plan"
    )
    tasks: list[TaskSchema] = Field(
        default_factory=list, description="Ordered list of research tasks"
    )
    dependencies: list[str] = Field(
        default_factory=list, description="Task execution sequence dependencies"
    )
    expected_output: str = Field(
        ..., description="Expected output artifact description"
    )
    estimated_steps: int = Field(
        default=1, description="Estimated total execution steps"
    )
    estimated_complexity: str = Field(
        default="medium",
        description="Overall research complexity (low, medium, high)",
    )
    clarification_required: bool = Field(
        default=False, description="Indicates if user clarification is required"
    )
    clarification_questions: list[str] = Field(
        default_factory=list,
        description="Questions for user if clarification is needed",
    )


PlanEnvelope = BaseResponse[PlannerResultSchema]
