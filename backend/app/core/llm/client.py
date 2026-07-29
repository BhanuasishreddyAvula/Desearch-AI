"""Reusable HTTPX-based OpenRouter client for the Desearch AI LLM Platform."""

import time
from typing import Any
import httpx

from app.core.config import settings
from app.core.llm.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConfigurationException,
    ExternalServiceException,
    RateLimitException,
    ResourceNotFoundException,
    ValidationException,
)
from app.core.llm.models import LLMRequest, LLMResponse
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger

logger = get_app_logger("core.llm")


class LLMClient:
    """Client for executing LLM completion requests against OpenRouter REST API."""

    def __init__(self) -> None:
        self.provider = "openrouter"

    def get_api_key(self) -> str | None:
        """Retrieve effective OpenRouter API key from configuration."""
        key = settings.OPENROUTER_API_KEY
        if key and key != "your_openrouter_api_key_placeholder":
            return key
        return None

    def generate_chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format_json: bool = True,
    ) -> LLMResponse:
        """Send chat completion request to OpenRouter REST API and return normalized LLMResponse."""
        request = LLMRequest(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model or settings.LLM_MODEL,
            temperature=temperature if temperature is not None else settings.TEMPERATURE,
            max_tokens=max_tokens or settings.MAX_TOKENS,
            response_format_json=response_format_json,
        )
        return self.execute_request(request)

    def execute_request(self, req: LLMRequest) -> LLMResponse:
        """Execute HTTP completion request against OpenRouter API endpoint."""
        api_key = self.get_api_key()
        if not api_key:
            logger.error("LLM Request Failed: OPENROUTER_API_KEY is missing")
            raise ConfigurationException(
                message="OPENROUTER_API_KEY is missing from server environment configuration",
                details={"provider": self.provider, "model": req.model},
            )

        active_model = req.model or settings.LLM_MODEL
        url = f"{settings.OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"
        timeout_seconds = settings.TIMEOUT_SECONDS or 60.0

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://desearch.ai",
            "X-Title": "Desearch AI",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": active_model,
            "messages": [
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.user_prompt},
            ],
            "temperature": req.temperature,
            "max_tokens": req.max_tokens,
        }

        if req.response_format_json:
            payload["response_format"] = {"type": "json_object"}

        start_time = time.perf_counter()
        logger.event(
            SystemEvents.AGENT_STARTED,
            f"LLM Request Started | Provider: {self.provider} | Model: {active_model}",
        )

        try:
            with httpx.Client(timeout=timeout_seconds) as http_client:
                response = http_client.post(url, json=payload, headers=headers)
                latency_ms = (time.perf_counter() - start_time) * 1000.0

                if response.status_code != 200:
                    self._handle_http_error(response, active_model, latency_ms)

                res_data = response.json()
                return self._parse_success_response(res_data, active_model, latency_ms)

        except (
            ConfigurationException,
            AuthenticationException,
            AuthorizationException,
            ResourceNotFoundException,
            RateLimitException,
            ValidationException,
            ExternalServiceException,
        ):
            raise
        except httpx.TimeoutException as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(
                "LLM Request Timeout | Provider: %s | Model: %s | Latency: %.2fms",
                self.provider,
                active_model,
                latency_ms,
            )
            raise ExternalServiceException(
                message=f"OpenRouter API request timed out after {timeout_seconds}s",
                error_code="LLM_TIMEOUT",
            ) from exc
        except httpx.RequestError as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.exception(
                "LLM Request Network Failure | Provider: %s | Model: %s | Latency: %.2fms | Error: %s",
                self.provider,
                active_model,
                latency_ms,
                str(exc),
            )
            raise ExternalServiceException(
                message=f"Network communication failure with OpenRouter API: {str(exc)}",
                error_code="LLM_NETWORK_ERROR",
            ) from exc
        except Exception as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.exception(
                "LLM Request System Error | Provider: %s | Model: %s | Latency: %.2fms | Error: %s",
                self.provider,
                active_model,
                latency_ms,
                str(exc),
            )
            raise ExternalServiceException(
                message=f"LLM Platform request failed: {str(exc)}",
                error_code="LLM_PROVIDER_ERROR",
            ) from exc

    def _parse_success_response(
        self, res_data: dict[str, Any], model: str, latency_ms: float
    ) -> LLMResponse:
        """Parse raw OpenRouter response dictionary into normalized LLMResponse."""
        try:
            choices = res_data.get("choices", [])
            if not choices or not choices[0].get("message", {}).get("content"):
                raise ExternalServiceException(
                    message="OpenRouter API returned an empty completion content payload",
                    error_code="LLM_EMPTY_RESPONSE",
                )

            content = str(choices[0]["message"]["content"]).strip()
            usage = res_data.get("usage", {})
            prompt_tokens = int(usage.get("prompt_tokens", 0))
            completion_tokens = int(usage.get("completion_tokens", 0))
            total_tokens = int(usage.get("total_tokens", prompt_tokens + completion_tokens))

            logger.event(
                SystemEvents.AGENT_COMPLETED,
                f"LLM Request Finished | Provider: {self.provider} | Model: {model} | "
                f"Latency: {latency_ms:.2f}ms | Status: 200 | "
                f"Tokens: prompt={prompt_tokens}, completion={completion_tokens}, total={total_tokens}",
            )

            return LLMResponse(
                content=content,
                model=model,
                provider=self.provider,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                latency_ms=latency_ms,
                raw_payload=res_data,
            )

        except ExternalServiceException:
            raise
        except Exception as exc:
            logger.error("Failed to parse OpenRouter completion response: %s", str(exc))
            raise ValidationException(
                message="OpenRouter completion payload failed parsing validation",
                details={"raw_response": res_data},
            ) from exc

    def _handle_http_error(
        self, response: httpx.Response, model: str, latency_ms: float
    ) -> None:
        """Map HTTP error status codes to standard application exception types."""
        status_code = response.status_code
        error_text = response.text
        logger.error(
            "LLM Request Failed | Provider: %s | Model: %s | Status: %d | Latency: %.2fms | Error: %s",
            self.provider,
            model,
            status_code,
            latency_ms,
            error_text,
        )

        if status_code == 401:
            raise AuthenticationException(
                message="Authentication failed: OPENROUTER_API_KEY is invalid or missing",
                details={"status_code": status_code, "raw_error": error_text},
            )
        if status_code == 403:
            raise AuthorizationException(
                message=f"Authorization failed: Forbidden access to requested model '{model}'",
                details={"status_code": status_code, "raw_error": error_text},
            )
        if status_code == 404:
            raise ResourceNotFoundException(
                message=f"Model '{model}' was not found on OpenRouter platform",
                details={"status_code": status_code, "raw_error": error_text},
            )
        if status_code == 429:
            raise RateLimitException(
                message="OpenRouter rate limit or quota exceeded. Please try again later.",
                details={"status_code": status_code, "raw_error": error_text},
            )
        if status_code in (408, 504):
            raise ExternalServiceException(
                message=f"OpenRouter Gateway request timed out (HTTP {status_code})",
                error_code="LLM_TIMEOUT",
                details={"status_code": status_code, "raw_error": error_text},
            )

        raise ExternalServiceException(
            message=f"OpenRouter API error (HTTP {status_code}): {error_text[:200]}",
            error_code="LLM_SERVICE_ERROR",
            details={"status_code": status_code, "raw_error": error_text},
        )
