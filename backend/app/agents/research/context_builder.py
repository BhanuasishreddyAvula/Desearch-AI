"""Bounded Research Context Builder and URL Deduplicator."""

from typing import Any
from urllib.parse import urlparse, urlunparse

from app.core.config import settings
from app.observability.logger import get_app_logger

logger = get_app_logger("agents.research.context_builder")


def normalize_url(url: str) -> str:
    """Safely normalize URL by stripping fragment anchors and trailing slashes."""
    if not url:
        return ""
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") if parsed.path != "/" else "/"
    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))


def safe_truncate_text(text: str, max_chars: int) -> tuple[str, bool]:
    """Truncate text to max_chars safely at paragraph or sentence boundary without breaking Unicode."""
    if not text or len(text) <= max_chars:
        return text, False

    truncated_raw = text[:max_chars]

    # Paragraph boundary check
    last_para = truncated_raw.rfind("\n\n")
    if last_para > max_chars * 0.7:
        return truncated_raw[:last_para].strip() + "\n\n[Content Truncated...]", True

    # Sentence boundary check
    last_sentence = truncated_raw.rfind(". ")
    if last_sentence > max_chars * 0.7:
        return (
            truncated_raw[: last_sentence + 1].strip() + " [Content Truncated...]",
            True,
        )

    # Word boundary check
    last_space = truncated_raw.rfind(" ")
    if last_space > max_chars * 0.7:
        return truncated_raw[:last_space].strip() + " [Content Truncated...]", True

    return truncated_raw.strip() + " [Content Truncated...]", True


class ResearchContextBuilder:
    """Builds execution-scoped deduplicated and bounded research context for LLM synthesis."""

    def __init__(
        self,
        max_source_chars: int | None = None,
        max_total_chars: int | None = None,
    ) -> None:
        self.max_source_chars = (
            max_source_chars or settings.RESEARCH_MAX_SOURCE_CHARS
        )
        self.max_total_chars = (
            max_total_chars or settings.RESEARCH_MAX_TOTAL_CHARS
        )
        self._extracted_cache: dict[str, dict[str, Any]] = {}
        self.duplicate_fetches_avoided = 0

    def get_cached_extraction(self, url: str) -> dict[str, Any] | None:
        """Return cached document extraction if URL was previously fetched in this execution run."""
        norm = normalize_url(url)
        if norm in self._extracted_cache:
            self.duplicate_fetches_avoided += 1
            logger.info(
                "Deduplication Hit | Reusing extracted content for URL: '%s'",
                norm,
            )
            return self._extracted_cache[norm]
        return None

    def cache_extraction(self, url: str, doc_data: dict[str, Any]) -> None:
        """Cache extracted document for current execution run."""
        norm = normalize_url(url)
        if norm:
            self._extracted_cache[norm] = doc_data

    def build_bounded_context(
        self,
        search_results: list[dict[str, Any]],
        extracted_documents: list[dict[str, Any]],
    ) -> tuple[str, dict[str, Any]]:
        """Construct bounded, formatted research context string adhering to source & total char limits."""
        formatted_sources: list[str] = []
        unique_urls: set[str] = set()

        raw_total_chars = 0
        included_total_chars = 0
        truncated_sources_count = 0

        # Step 1: Process search result snippets first
        for idx, item in enumerate(search_results):
            url = normalize_url(item.get("url", ""))
            if not url or url in unique_urls:
                continue
            unique_urls.add(url)

            title = item.get("title", "Untitled")
            snippet = item.get("snippet", "")
            raw_total_chars += len(snippet)

            bounded_snippet, is_truncated = safe_truncate_text(
                snippet, self.max_source_chars
            )
            if is_truncated:
                truncated_sources_count += 1

            if included_total_chars + len(bounded_snippet) > self.max_total_chars:
                logger.info(
                    "Global Context Budget Reached (%d chars) | Stopping search snippet inclusion",
                    self.max_total_chars,
                )
                break

            entry = (
                f"--- SEARCH SOURCE {len(unique_urls)} ---\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Snippet: {bounded_snippet}\n"
            )
            formatted_sources.append(entry)
            included_total_chars += len(entry)

        # Step 2: Process extracted webpage content
        for idx, doc in enumerate(extracted_documents):
            url = normalize_url(doc.get("url", ""))
            if not url:
                continue

            title = doc.get("title", f"Document ({url})")
            markdown = doc.get("markdown", "") or doc.get("plain_text", "")
            raw_total_chars += len(markdown)

            bounded_content, is_truncated = safe_truncate_text(
                markdown, self.max_source_chars
            )
            if is_truncated:
                truncated_sources_count += 1

            if included_total_chars + len(bounded_content) > self.max_total_chars:
                logger.info(
                    "Global Context Budget Reached (%d chars) | Stopping document content inclusion",
                    self.max_total_chars,
                )
                break

            entry = (
                f"\n--- EXTRACTED CONTENT ({url}) ---\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Content:\n{bounded_content}\n"
            )
            formatted_sources.append(entry)
            included_total_chars += len(entry)

        final_context_text = "\n".join(formatted_sources)

        metrics = {
            "sources_discovered": len(search_results),
            "unique_urls": len(unique_urls),
            "sources_extracted": len(extracted_documents),
            "duplicate_fetches_avoided": self.duplicate_fetches_avoided,
            "raw_characters": raw_total_chars,
            "included_characters": len(final_context_text),
            "truncated_sources": truncated_sources_count,
        }

        logger.info(
            "Research Context Built | Discovered: %d | Unique URLs: %d | Extracted: %d | Duplicates Avoided: %d | Raw Chars: %d | Included Chars: %d | Truncated: %d",
            metrics["sources_discovered"],
            metrics["unique_urls"],
            metrics["sources_extracted"],
            metrics["duplicate_fetches_avoided"],
            metrics["raw_characters"],
            metrics["included_characters"],
            metrics["truncated_sources"],
        )

        return final_context_text, metrics
