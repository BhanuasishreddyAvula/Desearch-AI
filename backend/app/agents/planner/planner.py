"""Planner Agent implementation using the normalized LLM Platform Client."""

import json

from app.agents.planner.models import PlannerResult, TaskModel
from app.agents.planner.prompts import (
    PLANNER_SYSTEM_PROMPT,
    build_planner_user_prompt,
)
from app.core.exceptions import ValidationException
from app.core.llm.client import LLMClient
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger

logger = get_app_logger("agents.planner")


class PlannerAgent:
    """AI agent responsible for formulating structured research execution plans via LLMClient."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def generate_plan(self, query: str, conversation_context: str = "") -> PlannerResult:
        """Formulate a research plan by sending prompts to the decoupled LLMClient."""
        logger.event(
            SystemEvents.AGENT_STARTED,
            f"Planner Agent starting plan generation for query: '{query[:60]}...'",
        )

        prompt = build_planner_user_prompt(query, conversation_context=conversation_context)

        # Execute normalized chat completion request via LLMClient (Specialized ultra-fast 0.2s planning model)
        response = self.llm_client.generate_chat_completion(
            system_prompt=PLANNER_SYSTEM_PROMPT,
            user_prompt=prompt,
            model="llama-3.1-8b-instant",
            response_format_json=True,
        )

        result = self._parse_json_response(query, response.content)

        logger.event(
            SystemEvents.AGENT_COMPLETED,
            f"Planning Completed | Tasks: {len(result.tasks)} | Provider: {response.provider} | Model: {response.model}",
        )
        return result

    def _parse_json_response(
        self, query: str, response_text: str
    ) -> PlannerResult:
        """Parse raw JSON string from LLM content into PlannerResult model."""
        try:
            cleaned_json = response_text.strip()
            if cleaned_json.startswith("```json"):
                cleaned_json = (
                    cleaned_json.removeprefix("```json")
                    .removesuffix("```")
                    .strip()
                )

            data = json.loads(cleaned_json)

            # Dynamic Entity Keyword Extraction to prevent search query drift
            import re
            stop_words = {"what", "is", "the", "difference", "between", "and", "or", "how", "to", "about", "them", "which", "for", "with", "a", "an", "in", "of", "on"}
            query_words = re.findall(r'\b[a-zA-Z0-9.\-+#]+\b', query.lower())
            core_entities = [w for w in query_words if w not in stop_words and len(w) > 1][:4]
            entity_str = " ".join(core_entities)

            raw_tasks = data.get("tasks", [])
            tasks = []
            for idx, t in enumerate(raw_tasks):
                if isinstance(t, str):
                    tasks.append(
                        TaskModel(
                            id=f"task_{idx+1}",
                            title=f"Task {idx+1}",
                            description=f"{t} ({entity_str})".strip() if entity_str else t,
                            priority="medium",
                            reason="Planned step",
                        )
                    )
                elif isinstance(t, dict):
                    desc = str(t.get("description", ""))
                    # Ground description with entity keywords if missing
                    if entity_str and not any(ent in desc.lower() for ent in core_entities):
                        desc = f"{desc} ({entity_str})".strip()

                    tasks.append(
                        TaskModel(
                            id=str(t.get("id", f"task_{idx+1}")),
                            title=str(t.get("title", f"Task {idx+1}")),
                            description=desc,
                            priority=str(t.get("priority", "medium")),
                            reason=str(t.get("reason", "")),
                        )
                    )


            return PlannerResult(
                goal=str(data.get("goal", query)),
                summary=str(data.get("summary", "Structured research plan")),
                tasks=tasks,
                dependencies=list(data.get("dependencies", [])),
                expected_output=str(
                    data.get(
                        "expected_output", "Markdown report with citations"
                    )
                ),
                estimated_steps=int(
                    data.get("estimated_steps", len(tasks) or 1)
                ),
                estimated_complexity=str(
                    data.get("estimated_complexity", "medium")
                ),
                clarification_required=bool(
                    data.get("clarification_required", False)
                ),
                clarification_questions=list(
                    data.get("clarification_questions", [])
                ),
            )

        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(
                "Planning Failed: Invalid JSON output from LLM: %s", str(exc)
            )
            raise ValidationException(
                message="Planner Agent produced invalid JSON output",
                details={"raw_response": response_text},
            ) from exc
