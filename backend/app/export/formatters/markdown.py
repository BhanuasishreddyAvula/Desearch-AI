"""Markdown report export formatter."""

from typing import Any

from app.export.formatters.base import BaseExportFormatter
from app.export.models import ExportResult


class MarkdownExportFormatter(BaseExportFormatter):
    """Formats report data into canonical Markdown document bytes."""

    def format_report(
        self, report_data: dict[str, Any], session_id: str
    ) -> ExportResult:
        """Format report data into UTF-8 encoded Markdown document."""
        full_md = report_data.get("full_markdown", "")

        if not full_md:
            # Reconstruct clean Markdown if full_markdown is missing
            title = report_data.get("title", "Research Report")
            exec_summary = report_data.get("executive_summary", "")
            sections = report_data.get("sections", [])
            sources = report_data.get("sources_cited", [])

            md_lines = [f"# {title}\n"]
            if exec_summary:
                md_lines.append(f"## Executive Summary\n\n{exec_summary}\n")

            for sec in sections:
                level_prefix = "#" * max(2, int(sec.get("level", 2)))
                md_lines.append(f"{level_prefix} {sec.get('title', '')}\n\n{sec.get('content', '')}\n")

            if sources:
                md_lines.append("## Sources & Citations\n")
                for src in sources:
                    md_lines.append(f"- [{src}]({src})")
                md_lines.append("")

            full_md = "\n".join(md_lines)

        filename = self.sanitize_filename(
            report_data.get("title", ""), session_id, "md"
        )
        content_bytes = full_md.encode("utf-8")

        return ExportResult(
            content=content_bytes,
            media_type="text/markdown; charset=utf-8",
            filename=filename,
        )
