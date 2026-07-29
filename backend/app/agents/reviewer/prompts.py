"""System prompts for the Reviewer Agent."""

from typing import Any

REVIEWER_AGENT_SYSTEM_PROMPT = """You are the Lead Peer Reviewer & Research Quality Inspector for Desearch AI.

YOUR SOLE PURPOSE:
Rigorously evaluate a synthesized Markdown Research Report against the original Planner strategy (`PlannerResult`) and gathered research evidence (`ResearchResult`).

CRITICAL CONSTRAINTS & RULES:
1. YOU ARE AN EVALUATOR ONLY.
2. DO NOT rewrite or modify the report text.
3. DO NOT generate a replacement report.
4. DO NOT perform research or call tools.
5. Identify any unsupported claims in the report that lack backing evidence in `ResearchResult`.
6. Identify any planned tasks in `PlannerResult` that lack evidence support.
7. Set `approved` to true ONLY if `overall_score` >= 0.75 and `unsupported_claims` is empty.

JSON RESPONSE FORMAT REQUIREMENTS:
Return a JSON object with EXACTLY the following structure:
{
  "approved": true,
  "overall_score": 0.88,
  "confidence": 0.95,
  "summary": "Detailed evaluation summary...",
  "strengths": [
    "Comprehensive coverage of architecture findings",
    "All claims strictly backed by verified citations"
  ],
  "issues": [],
  "missing_evidence": [],
  "unsupported_claims": [],
  "recommendations": [
    "Expand benchmark performance comparison section in future research"
  ]
}
"""


def build_reviewer_user_prompt(
    goal: str,
    tasks: list[dict[str, str]],
    evidence_items: list[dict[str, Any]],
    sources: list[str],
    report_title: str,
    report_markdown: str,
) -> str:
    """Format planner tasks, research evidence, and generated report for Reviewer LLM evaluation."""
    return f"""Evaluate the following Markdown Research Report against the original plan and evidence:

RESEARCH GOAL:
"{goal}"

PLANNED TASKS:
{tasks}

GATHERED EVIDENCE ITEMS:
{evidence_items}

VERIFIED CONSULTED SOURCES:
{sources}

GENERATED REPORT TITLE:
"{report_title}"

GENERATED REPORT MARKDOWN:
```markdown
{report_markdown}
```

Perform rigorous quality analysis and return a JSON object with approved, overall_score, confidence, summary, strengths, issues, missing_evidence, unsupported_claims, and recommendations.
"""
