"""Writer Agent implementation synthesizing research evidence into Markdown reports."""

import json
from typing import Any

from app.agents.planner.models import PlannerResult
from app.agents.research.models import ResearchResult
from app.agents.writer.models import ReportMetadata, ReportResult, ReportSection
from app.agents.writer.prompts import (
    WRITER_AGENT_SYSTEM_PROMPT,
    build_writer_user_prompt,
)
from app.core.exceptions import ValidationException
from app.core.llm.client import LLMClient
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger

logger = get_app_logger("agents.writer")


class WriterAgent:
    """AI agent responsible for transforming structured research evidence into Markdown reports."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def write_report(
        self,
        session_id: str,
        planner_result: PlannerResult,
        research_result: ResearchResult,
    ) -> ReportResult:
        """Synthesize Planner and Research results into a structured ReportResult."""
        logger.event(
            SystemEvents.AGENT_STARTED,
            f"Writer Started | Session: {session_id} | Goal: '{planner_result.goal[:60]}...'",
        )

        evidence_payloads: list[dict[str, Any]] = [
            ev.to_dict() for ev in research_result.evidence_items
        ]

        prompt = build_writer_user_prompt(
            goal=planner_result.goal,
            planner_summary=planner_result.summary,
            evidence_items=evidence_payloads,
            sources=research_result.sources_consulted,
        )
        logger.info("Prompt Created | Session: %s", session_id)

        logger.info("LLM Started | Writer Agent calling LLMClient")
        llm_response = self.llm_client.generate_chat_completion(
            system_prompt=WRITER_AGENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format_json=True,
        )
        logger.info("LLM Finished | Latency: %.2fms", llm_response.latency_ms)

        result = self._parse_json_response(
            session_id, llm_response.content, research_result
        )

        logger.event(
            SystemEvents.AGENT_COMPLETED,
            f"Writer Completed | Report Generated | Title: '{result.title}' | Words: {result.metadata.word_count}",
        )
        return result

    def _parse_json_response(
        self,
        session_id: str,
        response_text: str,
        research_result: ResearchResult,
    ) -> ReportResult:
        """Parse raw JSON string from LLM response into ReportResult model."""
        try:
            cleaned_json = response_text.strip()
            if cleaned_json.startswith("```json"):
                cleaned_json = (
                    cleaned_json.removeprefix("```json")
                    .removesuffix("```")
                    .strip()
                )

            data = json.loads(cleaned_json)

            sections = [
                ReportSection(
                    title=str(sec.get("title", f"Section {idx+1}")),
                    content=str(sec.get("content", "")),
                    level=int(sec.get("level", 2)),
                )
                for idx, sec in enumerate(data.get("sections", []))
            ]

            full_markdown = str(data.get("full_markdown", ""))
            if not full_markdown and sections:
                full_markdown = (
                    f"# {data.get('title', 'Research Report')}\n\n"
                    + "\n\n".join(
                        f"{'#' * sec.level} {sec.title}\n\n{sec.content}"
                        for sec in sections
                    )
                )

            sources_cited = (
                list(data.get("sources_cited", []))
                or research_result.sources_consulted
            )
            word_count = len(full_markdown.split())

            metadata = ReportMetadata(
                word_count=word_count,
                sections_count=len(sections),
                evidence_cited_count=len(research_result.evidence_items),
                sources_count=len(sources_cited),
            )

            return ReportResult(
                session_id=session_id,
                title=str(data.get("title", "Desearch AI Research Report")),
                executive_summary=str(data.get("executive_summary", "")),
                full_markdown=full_markdown,
                sections=sections,
                sources_cited=sources_cited,
                metadata=metadata,
            )

        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(
                "Failed to parse Writer Agent JSON output: %s", str(exc)
            )
            raise ValidationException(
                message="Writer Agent produced invalid JSON output",
                details={"raw_response": response_text},
            ) from exc
