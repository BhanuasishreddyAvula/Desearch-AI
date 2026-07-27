"""Global FastAPI exception handlers formatting errors as standard ErrorResponse."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import AppException
from app.observability.context import get_trace_id
from app.observability.logger import get_app_logger
from app.schemas.error import ErrorDetails, ErrorResponse
from app.schemas.metadata import ResponseMetadata

logger = get_app_logger("exception_handler")


def create_error_response(
    status_code: int,
    message: str,
    error_code: str,
    error_type: str,
    details: Any = None,
    request: Request | None = None,
    trace_id: str | None = None,
) -> JSONResponse:
    """Helper function building standardized JSONResponse wrapping ErrorResponse schema."""
    request_id: str | None = None
    execution_time_ms: float = 0.0

    if request is not None:
        request_id = getattr(request.state, "request_id", None)
        execution_time_ms = getattr(request.state, "execution_time_ms", 0.0)

    effective_trace_id = trace_id or get_trace_id()

    error_payload = ErrorResponse(
        success=False,
        message=message,
        request_id=request_id,
        data=ErrorDetails(
            error_code=error_code,
            error_type=error_type,
            details=details,
            trace_id=effective_trace_id,
        ),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
    return JSONResponse(
        status_code=status_code,
        content=error_payload.model_dump(mode="json"),
    )


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for custom application exceptions (AppException and subclasses)."""
    app_exc: AppException = exc if isinstance(exc, AppException) else AppException(str(exc))
    logger.warning(
        "Application exception [%s]: %s (path: %s)",
        app_exc.error_code,
        app_exc.message,
        request.url.path,
    )
    return create_error_response(
        status_code=app_exc.status_code,
        message=app_exc.message,
        error_code=app_exc.error_code,
        error_type=app_exc.error_type,
        details=app_exc.details,
        request=request,
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for standard FastAPI/Starlette HTTPExceptions."""
    http_exc: HTTPException = (
        exc if isinstance(exc, HTTPException) else HTTPException(status_code=500, detail=str(exc))
    )
    error_code = "HTTP_ERROR"
    error_type = "CLIENT_ERROR" if http_exc.status_code < 500 else "SERVER_ERROR"

    logger.warning(
        "HTTP exception status %d: %s (path: %s)",
        http_exc.status_code,
        http_exc.detail,
        request.url.path,
    )

    return create_error_response(
        status_code=http_exc.status_code,
        message=str(http_exc.detail),
        error_code=error_code,
        error_type=error_type,
        request=request,
    )


async def request_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for FastAPI request validation errors (invalid query/body/path params)."""
    val_exc: RequestValidationError = (
        exc if isinstance(exc, RequestValidationError) else RequestValidationError([])
    )
    formatted_errors: list[dict[str, Any]] = []
    for err in val_exc.errors():
        location = " -> ".join(str(loc) for loc in err.get("loc", []))
        formatted_errors.append(
            {
                "field": location,
                "message": err.get("msg", "Validation error"),
                "type": err.get("type", "value_error"),
            }
        )

    logger.warning(
        "Request validation failed for %s: %d error(s)",
        request.url.path,
        len(formatted_errors),
    )

    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Request parameters or body failed validation",
        error_code="VALIDATION_FAILED",
        error_type="REQUEST_VALIDATION_ERROR",
        details=formatted_errors,
        request=request,
    )


async def pydantic_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for Pydantic schema validation errors."""
    formatted_errors: list[dict[str, Any]] = []
    if isinstance(exc, ValidationError):
        for err in exc.errors():
            location = " -> ".join(str(loc) for loc in err.get("loc", []))
            formatted_errors.append(
                {
                    "field": location,
                    "message": err.get("msg", "Validation error"),
                    "type": err.get("type", "value_error"),
                }
            )

    logger.warning(
        "Pydantic validation failed for %s: %d error(s)",
        request.url.path,
        len(formatted_errors),
    )

    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Data schema validation failed",
        error_code="SCHEMA_VALIDATION_ERROR",
        error_type="DATA_VALIDATION_ERROR",
        details=formatted_errors,
        request=request,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unexpected unhandled exceptions."""
    logger.exception("Unhandled internal exception on %s: %s", request.url.path, str(exc))

    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected internal server error occurred",
        error_code="INTERNAL_SERVER_ERROR",
        error_type="SYSTEM_ERROR",
        details=None,
        request=request,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI application instance."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
