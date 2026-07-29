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
        """Parse raw JSON string or raw Markdown from LLM response into ReportResult model."""
        cleaned_json = response_text.strip()
        if cleaned_json.startswith("```"):
            lines = cleaned_json.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned_json = "\n".join(lines).strip()

        if not cleaned_json.startswith("{"):
            start_idx = cleaned_json.find("{")
            end_idx = cleaned_json.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                cleaned_json = cleaned_json[start_idx : end_idx + 1]

        try:
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
            logger.warning(
                "Writer Agent JSON parse failed (%s). Attempting raw markdown fallback...",
                str(exc),
            )
            return self._build_raw_markdown_fallback(
                session_id, response_text, research_result
            )

    def _build_raw_markdown_fallback(
        self,
        session_id: str,
        response_text: str,
        research_result: ResearchResult,
    ) -> ReportResult:
        """Fallback parser constructing ReportResult directly from raw Markdown LLM response."""
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```"):
            lines = cleaned_text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned_text = "\n".join(lines).strip()

        lines = cleaned_text.splitlines()
        title = "Desearch AI Research Report"
        for line in lines:
            if line.startswith("# "):
                title = line.removeprefix("# ").strip()
                break

        sections: list[ReportSection] = []
        current_title = "Executive Summary"
        current_content: list[str] = []
        current_level = 2

        for line in lines:
            if line.startswith("## "):
                if current_content:
                    sections.append(
                        ReportSection(
                            title=current_title,
                            content="\n".join(current_content).strip(),
                            level=current_level,
                        )
                    )
                current_title = line.removeprefix("## ").strip()
                current_content = []
            elif line.startswith("# "):
                continue
            else:
                current_content.append(line)

        if current_content:
            sections.append(
                ReportSection(
                    title=current_title,
                    content="\n".join(current_content).strip(),
                    level=current_level,
                )
            )

        if not sections:
            sections.append(
                ReportSection(
                    title="Findings",
                    content=cleaned_text,
                    level=2,
                )
            )

        exec_summary = sections[0].content[:500] if sections else cleaned_text[:500]
        sources_cited = research_result.sources_consulted

        word_count = len(cleaned_text.split())
        metadata = ReportMetadata(
            word_count=word_count,
            sections_count=len(sections),
            evidence_cited_count=len(research_result.evidence_items),
            sources_count=len(sources_cited),
        )

        return ReportResult(
            session_id=session_id,
            title=title,
            executive_summary=exec_summary,
            full_markdown=cleaned_text,
            sections=sections,
            sources_cited=sources_cited,
            metadata=metadata,
        )
