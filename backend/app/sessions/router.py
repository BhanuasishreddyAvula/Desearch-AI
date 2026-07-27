"""API router for Research Session management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.repositories.session import AbstractSessionRepository
from app.dependencies import (
    get_execution_time_dep,
    get_request_id_dep,
    get_session_repository_dep,
)
from app.schemas.base import BaseResponse
from app.schemas.metadata import ResponseMetadata
from app.sessions.models import ResearchSession
from app.sessions.schemas import (
    CreateSessionRequest,
    SessionListResponse,
    SessionResponse,
    UpdateSessionRequest,
)
from app.sessions.service import SessionService

router = APIRouter(tags=["Sessions"])


def get_session_service(
    repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
) -> SessionService:
    """Dependency provider for SessionService injecting the abstract repository interface."""
    return SessionService(repository=repo)


def _to_session_response(session: ResearchSession) -> SessionResponse:
    """Convert domain ResearchSession entity into API SessionResponse schema."""
    return SessionResponse(
        id=session.id,
        title=session.title,
        query=session.query,
        status=session.status,
        created_at=session.created_at,
        updated_at=session.updated_at,
        metadata=session.metadata,
    )


@router.post(
    "",
    response_model=BaseResponse[SessionResponse],
    summary="Create Research Session",
    description="Initialize a new research session with a primary query in DRAFT state.",
)
async def create_session(
    data: CreateSessionRequest,
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> BaseResponse[SessionResponse]:
    """Create session endpoint."""
    session = service.create_session(data)
    return BaseResponse(
        success=True,
        message="Research session created successfully.",
        request_id=request_id,
        data=_to_session_response(session),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )


@router.get(
    "",
    response_model=BaseResponse[SessionListResponse],
    summary="List Research Sessions",
    description="Retrieve all stored research sessions.",
)
async def list_sessions(
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> BaseResponse[SessionListResponse]:
    """List sessions endpoint."""
    sessions, total = service.list_sessions()
    response_data = SessionListResponse(
        sessions=[_to_session_response(s) for s in sessions],
        total=total,
    )
    return BaseResponse(
        success=True,
        message="Research sessions retrieved successfully.",
        request_id=request_id,
        data=response_data,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )


@router.get(
    "/{session_id}",
    response_model=BaseResponse[SessionResponse],
    summary="Get Research Session",
    description="Retrieve a specific research session by ID.",
)
async def get_session(
    session_id: str,
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> BaseResponse[SessionResponse]:
    """Get session by ID endpoint."""
    session = service.get_session(session_id)
    return BaseResponse(
        success=True,
        message="Research session retrieved successfully.",
        request_id=request_id,
        data=_to_session_response(session),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )


@router.patch(
    "/{session_id}",
    response_model=BaseResponse[SessionResponse],
    summary="Update Research Session",
    description="Update session title, metadata, or transition lifecycle status.",
)
async def update_session(
    session_id: str,
    data: UpdateSessionRequest,
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> BaseResponse[SessionResponse]:
    """Update session endpoint."""
    session = service.update_session(session_id, data)
    return BaseResponse(
        success=True,
        message="Research session updated successfully.",
        request_id=request_id,
        data=_to_session_response(session),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
