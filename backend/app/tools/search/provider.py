"""Exa Provider implementation executing web search queries via Exa REST API."""

import time
from typing import Any
import httpx

from app.core.config import settings
from app.observability.logger import get_app_logger
from app.tools.search.exceptions import (
    SearchAuthenticationException,
    SearchAuthorizationException,
    SearchException,
    SearchNotFoundException,
    SearchRateLimitException,
    SearchTimeoutException,
)
from app.tools.search.models import SearchResult, SearchResultItem

logger = get_app_logger("tools.search.exa")


class ExaProvider:
    """Exa Search API provider handling direct HTTP interactions with Exa REST API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key or settings.EXA_API_KEY
        self.base_url = (base_url or settings.EXA_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.SEARCH_TIMEOUT

    def search(self, query: str, max_results: int = 5) -> SearchResult:
        """Perform search query via Exa API and return normalized SearchResult."""
        start_time = time.perf_counter()

        if not self.api_key:
            logger.error("Exa Search Configuration Error | EXA_API_KEY is missing or empty")
            raise SearchAuthenticationException(
                message="EXA_API_KEY is missing or unconfigured in environment settings."
            )

        logger.info("Search Started | Provider: Exa | Query: '%s'", query[:60])
        endpoint = f"{self.base_url}/search"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        payload: dict[str, Any] = {
            "query": query,
            "numResults": max_results,
            "useAutoprompt": True,
            "contents": {"text": True},
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(endpoint, json=payload, headers=headers)
                latency_ms = (time.perf_counter() - start_time) * 1000.0
                status_code = response.status_code

                logger.info(
                    "Search Completed | Provider: Exa | Latency: %.2fms | HTTP Status: %d",
                    latency_ms,
                    status_code,
                )

                if status_code == 200:
                    data = response.json()
                    raw_results = data.get("results", [])
                    items: list[SearchResultItem] = []

                    for res in raw_results:
                        items.append(
                            SearchResultItem(
                                title=str(res.get("title", "Untitled")),
                                url=str(res.get("url", "")),
                                snippet=str(res.get("text", res.get("snippet", ""))),
                                published_at=res.get("publishedDate"),
                                score=float(res["score"])
                                if "score" in res and res["score"] is not None
                                else None,
                                metadata={
                                    "id": res.get("id"),
                                    "author": res.get("author"),
                                },
                            )
                        )

                    return SearchResult(
                        query=query,
                        results=items,
                        total_results=len(items),
                        latency_ms=latency_ms,
                    )

                self._handle_error_status(status_code, response.text)

        except httpx.TimeoutException as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error("Exa Search Timeout | Latency: %.2fms | Error: %s", latency_ms, str(exc))
            raise SearchTimeoutException(
                message=f"Exa Search request timed out after {self.timeout}s"
            ) from exc
        except httpx.RequestError as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error("Exa Search Connection Failure | Latency: %.2fms | Error: %s", latency_ms, str(exc))
            raise SearchException(
                message=f"Exa Search HTTP request failed: {str(exc)}"
            ) from exc

    def _handle_error_status(self, status_code: int, response_text: str) -> None:
        """Map HTTP error status codes to standardized application exceptions."""
        error_msg = f"Exa Search API returned status {status_code}: {response_text[:200]}"
        if status_code == 401:
            raise SearchAuthenticationException(message=error_msg)
        elif status_code == 403:
            raise SearchAuthorizationException(message=error_msg)
        elif status_code == 404:
            raise SearchNotFoundException(message=error_msg)
        elif status_code in (408, 504):
            raise SearchTimeoutException(message=error_msg)
        elif status_code == 429:
            raise SearchRateLimitException(message=error_msg)
        else:
            raise SearchException(message=error_msg)
