"""Reviewer Agent implementation evaluating report quality and evidence validity."""

import json
from typing import Any

from app.agents.planner.models import PlannerResult
from app.agents.research.models import ResearchResult
from app.agents.reviewer.models import ReviewResult
from app.agents.reviewer.prompts import (
    REVIEWER_AGENT_SYSTEM_PROMPT,
    build_reviewer_user_prompt,
)
from app.agents.writer.models import ReportResult
from app.core.exceptions import ValidationException
from app.core.llm.client import LLMClient
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger

logger = get_app_logger("agents.reviewer")


class ReviewerAgent:
    """AI agent responsible for evaluating report quality and verifying evidence alignment."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def review_report(
        self,
        session_id: str,
        planner_result: PlannerResult,
        research_result: ResearchResult,
        report_result: ReportResult,
    ) -> ReviewResult:
        """Evaluate ReportResult against PlannerResult and ResearchResult evidence."""
        logger.event(
            SystemEvents.AGENT_STARTED,
            f"Reviewer Started | Session: {session_id} | Report: '{report_result.title[:60]}...'",
        )

        tasks_payload = [
            {"id": t.id, "title": t.title, "description": t.description}
            for t in planner_result.tasks
        ]
        evidence_payloads: list[dict[str, Any]] = [
            ev.to_dict() for ev in research_result.evidence_items
        ]

        prompt = build_reviewer_user_prompt(
            goal=planner_result.goal,
            tasks=tasks_payload,
            evidence_items=evidence_payloads,
            sources=research_result.sources_consulted,
            report_title=report_result.title,
            report_markdown=report_result.full_markdown,
        )
        logger.info("Prompt Created | Session: %s", session_id)

        logger.info("LLM Started | Reviewer Agent calling LLMClient")
        llm_response = self.llm_client.generate_chat_completion(
            system_prompt=REVIEWER_AGENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format_json=True,
        )
        logger.info("LLM Finished | Latency: %.2fms", llm_response.latency_ms)

        result = self._parse_json_response(session_id, llm_response.content)

        logger.info(
            "Review Completed | Session: %s | Approved: %s | Score: %.2f",
            session_id,
            result.approved,
            result.overall_score,
        )
        logger.event(
            SystemEvents.AGENT_COMPLETED,
            f"Reviewer Finished | Session: {session_id} | Approved: {result.approved} | Score: {result.overall_score:.2f}",
        )
        return result

    def _parse_json_response(
        self, session_id: str, response_text: str
    ) -> ReviewResult:
        """Parse raw JSON string from LLM response into ReviewResult model."""
        try:
            cleaned_json = response_text.strip()
            if cleaned_json.startswith("```json"):
                cleaned_json = (
                    cleaned_json.removeprefix("```json")
                    .removesuffix("```")
                    .strip()
                )

            data = json.loads(cleaned_json)

            score = float(data.get("overall_score", 0.85))
            unsupported = list(data.get("unsupported_claims", []))
            approved = bool(
                data.get("approved", score >= 0.75 and len(unsupported) == 0)
            )

            return ReviewResult(
                session_id=session_id,
                approved=approved,
                overall_score=score,
                confidence=float(data.get("confidence", 0.90)),
                summary=str(
                    data.get(
                        "summary",
                        "Quality evaluation completed successfully.",
                    )
                ),
                strengths=list(data.get("strengths", [])),
                issues=list(data.get("issues", [])),
                missing_evidence=list(data.get("missing_evidence", [])),
                unsupported_claims=unsupported,
                recommendations=list(data.get("recommendations", [])),
            )

        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(
                "Failed to parse Reviewer Agent JSON output: %s", str(exc)
            )
            raise ValidationException(
                message="Reviewer Agent produced invalid JSON output",
                details={"raw_response": response_text},
            ) from exc
