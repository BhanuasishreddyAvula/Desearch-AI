"""Research Agent implementation querying ToolRegistry and structuring bounded evidence."""

from collections.abc import Callable
import json
from typing import Any

from app.agents.research.context_builder import (
    ResearchContextBuilder,
    normalize_url,
)
from app.agents.research.models import Evidence, EvidenceCollection, ResearchResult
from app.agents.research.prompts import (
    RESEARCH_AGENT_SYSTEM_PROMPT,
    build_research_user_prompt,
)
from app.core.exceptions import (
    ResourceNotFoundException,
    ValidationException,
)
from app.core.llm.client import LLMClient
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger
from app.tools.registry import ToolRegistry

logger = get_app_logger("agents.research")


class ResearchAgent:
    """AI agent responsible for executing research tasks via ToolRegistry and assembling evidence."""

    def __init__(self, llm_client: LLMClient, tool_registry: ToolRegistry) -> None:
        self.llm_client = llm_client
        self.tool_registry = tool_registry

    def run_research(
        self,
        session_id: str,
        goal: str,
        tasks: list[dict[str, str]],
        on_progress: Callable[[str, str, dict[str, Any]], None] | None = None,
    ) -> ResearchResult:
        """Execute research tasks using tools from ToolRegistry and return structured ResearchResult."""
        logger.event(
            SystemEvents.AGENT_STARTED,
            f"Research Started | Session: {session_id} | Goal: '{goal[:60]}...'",
        )

        context_builder = ResearchContextBuilder()
        tools_executed: set[str] = set()
        sources_consulted: set[str] = set()

        all_search_items: list[dict[str, Any]] = []
        all_extracted_docs: list[dict[str, Any]] = []

        # Step 1: Obtain web_search tool from ToolRegistry
        if not self.tool_registry.exists("web_search"):
            logger.error("Missing Tool | Requested tool 'web_search' not registered")
            raise ResourceNotFoundException(
                message="Tool 'web_search' requested by Research Agent is not registered."
            )

        search_tool = self.tool_registry.get("web_search")
        if not search_tool or not search_tool.enabled:
            logger.error("Disabled Tool | Requested tool 'web_search' is disabled")
            raise ValidationException(
                message="Tool 'web_search' requested by Research Agent is disabled."
            )

        # Check if content extraction tool web_fetch is available
        content_tool = (
            self.tool_registry.get("web_fetch")
            if self.tool_registry.exists("web_fetch")
            else None
        )

        # Step 2: Execute Search & Content Extraction with Deduplication
        for idx, task in enumerate(tasks):
            task_title = task.get("title", f"Task {idx+1}")
            task_desc = task.get("description", goal)

            logger.info("Tool Requested | ID: web_search | Task: %s", task_title)
            if on_progress:
                on_progress(
                    "research.searching",
                    "Researching",
                    {"task": task_title, "query": task_desc[:40]},
                )

            search_res = search_tool.execute(query=task_desc, max_results=3)
            tools_executed.add("web_search")
            logger.info("Tool Returned | ID: web_search")

            raw_results = search_res.get("results", [])
            task_urls: list[str] = []

            for item in raw_results:
                if isinstance(item, dict):
                    all_search_items.append(item)
                    if "url" in item and item["url"]:
                        norm = normalize_url(item["url"])
                        sources_consulted.add(norm)
                        task_urls.append(norm)

            # Step 3: Execute Content Extraction (or reuse from execution cache)
            if content_tool and content_tool.enabled and task_urls:
                target_url = task_urls[0]

                # Execution-scoped URL Deduplication check
                cached_doc = context_builder.get_cached_extraction(target_url)
                if cached_doc:
                    tools_executed.add("web_fetch")
                    all_extracted_docs.append(cached_doc)
                else:
                    try:
                        logger.info("Tool Requested | ID: web_fetch | URL: %s", target_url)
                        if on_progress:
                            on_progress(
                                "research.extracting",
                                "Researching",
                                {"url": target_url},
                            )

                        content_res = content_tool.execute(url=target_url)
                        tools_executed.add("web_fetch")
                        logger.info("Tool Returned | ID: web_fetch")

                        doc_entry = {
                            "url": target_url,
                            "title": content_res.get("title", f"Document ({target_url})"),
                            "markdown": content_res.get("markdown", "") or content_res.get("plain_text", ""),
                        }
                        context_builder.cache_extraction(target_url, doc_entry)
                        all_extracted_docs.append(doc_entry)
                    except Exception as exc:
                        logger.warning(
                            "Content extraction failed for URL '%s': %s",
                            target_url,
                            str(exc),
                        )

        # Step 4: Construct Bounded Research Context
        bounded_context_text, metrics = context_builder.build_bounded_context(
            all_search_items, all_extracted_docs
        )

        # Step 5: Use LLMClient to process bounded context into structured evidence
        prompt = build_research_user_prompt(goal, tasks, bounded_context_text)
        llm_response = self.llm_client.generate_chat_completion(
            system_prompt=RESEARCH_AGENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format_json=True,
        )

        result = self._parse_json_response(
            session_id,
            goal,
            llm_response.content,
            list(tools_executed),
            list(sources_consulted),
        )

        logger.event(
            SystemEvents.AGENT_COMPLETED,
            f"Research Completed | Evidence Added: {len(result.evidence_items)} | Tools: {len(result.tools_executed)} | Included Chars: {metrics['included_characters']}",
        )
        return result

    def _parse_json_response(
        self,
        session_id: str,
        goal: str,
        response_text: str,
        tools_executed: list[str],
        sources_consulted: list[str],
    ) -> ResearchResult:
        """Parse raw JSON string from LLM response into ResearchResult model."""
        try:
            cleaned_json = response_text.strip()
            if cleaned_json.startswith("```json"):
                cleaned_json = (
                    cleaned_json.removeprefix("```json")
                    .removesuffix("```")
                    .strip()
                )

            data = json.loads(cleaned_json)
            collection = EvidenceCollection()

            raw_items = data.get("evidence_items", [])
            for idx, item in enumerate(raw_items):
                ev = Evidence(
                    id=str(item.get("id", f"ev_{idx+1}")),
                    title=str(item.get("title", f"Evidence {idx+1}")),
                    summary=str(item.get("summary", "")),
                    source=str(
                        item.get(
                            "source",
                            sources_consulted[0]
                            if sources_consulted
                            else "https://exa.ai",
                        )
                    ),
                    tool_used=str(item.get("tool_used", "web_search")),
                    confidence=float(item.get("confidence", 0.85)),
                    metadata=dict(item.get("metadata", {})),
                )
                collection.add(ev)
                logger.info("Evidence Added | ID: %s | Source: %s", ev.id, ev.source)

            res_sources = list(data.get("sources_consulted", [])) or sources_consulted
            res_tools = list(data.get("tools_executed", [])) or tools_executed

            return ResearchResult(
                session_id=session_id,
                goal=goal,
                summary=str(
                    data.get(
                        "summary", "Structured research evidence collection"
                    )
                ),
                evidence_items=collection.list_all(),
                sources_consulted=res_sources,
                tools_executed=res_tools,
            )

        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Failed to parse Research Agent JSON output: %s", str(exc))
            raise ValidationException(
                message="Research Agent produced invalid JSON output",
                details={"raw_response": response_text},
            ) from exc
