"""Firecrawl Provider implementation extracting web page content via Firecrawl REST API."""

import time
from typing import Any
import httpx

from app.core.config import settings
from app.observability.logger import get_app_logger
from app.tools.content.exceptions import (
    ContentAuthenticationException,
    ContentAuthorizationException,
    ContentException,
    ContentNotFoundException,
    ContentRateLimitException,
    ContentTimeoutException,
)
from app.tools.content.models import ExtractedDocument

logger = get_app_logger("tools.content.firecrawl")


class FirecrawlProvider:
    """Firecrawl API provider handling direct web extraction HTTP interactions."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key or settings.FIRECRAWL_API_KEY
        self.base_url = (base_url or settings.FIRECRAWL_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.CONTENT_TIMEOUT

    def scrape(self, url: str) -> ExtractedDocument:
        """Extract web page markdown content via Firecrawl API."""
        start_time = time.perf_counter()

        if not self.api_key:
            logger.error("Firecrawl Extraction Configuration Error | FIRECRAWL_API_KEY is missing or empty")
            raise ContentAuthenticationException(
                message="FIRECRAWL_API_KEY is missing or unconfigured in environment settings."
            )

        logger.info("Content Extraction Started | Provider: Firecrawl | URL: '%s'", url)
        endpoint = f"{self.base_url}/v1/scrape"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        payload: dict[str, Any] = {
            "url": url,
            "formats": ["markdown"],
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(endpoint, json=payload, headers=headers)
                latency_ms = (time.perf_counter() - start_time) * 1000.0
                status_code = response.status_code

                logger.info(
                    "Content Extraction Completed | Provider: Firecrawl | Latency: %.2fms | HTTP Status: %d",
                    latency_ms,
                    status_code,
                )

                if status_code == 200:
                    data = response.json()
                    doc_data = data.get("data", {})
                    metadata = doc_data.get("metadata", {})
                    markdown = str(doc_data.get("markdown", ""))
                    title = str(metadata.get("title", f"Document ({url})"))

                    return ExtractedDocument(
                        url=url,
                        title=title,
                        markdown=markdown,
                        plain_text=markdown.replace("#", "").replace("*", "").strip(),
                        metadata=metadata,
                    )

                self._handle_error_status(status_code, response.text)

        except httpx.TimeoutException as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error("Firecrawl Extraction Timeout | Latency: %.2fms | Error: %s", latency_ms, str(exc))
            raise ContentTimeoutException(
                message=f"Firecrawl extraction request timed out after {self.timeout}s"
            ) from exc
        except httpx.RequestError as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error("Firecrawl Extraction Connection Failure | Latency: %.2fms | Error: %s", latency_ms, str(exc))
            raise ContentException(
                message=f"Firecrawl HTTP extraction failed: {str(exc)}"
            ) from exc

    def _handle_error_status(self, status_code: int, response_text: str) -> None:
        """Map HTTP error status codes to standardized application exceptions."""
        error_msg = f"Firecrawl API returned status {status_code}: {response_text[:200]}"
        if status_code == 401:
            raise ContentAuthenticationException(message=error_msg)
        elif status_code == 403:
            raise ContentAuthorizationException(message=error_msg)
        elif status_code == 404:
            raise ContentNotFoundException(message=error_msg)
        elif status_code in (408, 504):
            raise ContentTimeoutException(message=error_msg)
        elif status_code == 429:
            raise ContentRateLimitException(message=error_msg)
        else:
            raise ContentException(message=error_msg)
