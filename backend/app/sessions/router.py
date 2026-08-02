"""API router for Research Session management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.conversations.repository import AbstractConversationRepository
from app.conversations.schemas import (
    ConversationMessageResponse,
    ConversationMessagesListResponse,
)
from app.core.config import settings
from app.core.repositories.session import AbstractSessionRepository
from app.dependencies import (
    get_conversation_repository_dep,
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
        device_id=session.device_id,
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
    x_device_id: Annotated[str, Header(alias="X-Device-ID")] = "",
) -> BaseResponse[SessionResponse]:
    """Create session endpoint."""
    session = service.create_session(data, device_id=x_device_id)
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
    description="Retrieve all research sessions belonging to the requesting device.",
)
async def list_sessions(
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
    x_device_id: Annotated[str, Header(alias="X-Device-ID")] = "",
) -> BaseResponse[SessionListResponse]:
    """List sessions endpoint — returns only sessions owned by the requesting device."""
    sessions, total = service.list_sessions(device_id=x_device_id)
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
    description="Retrieve a specific research session by ID, enforcing device ownership.",
)
async def get_session(
    session_id: str,
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
    x_device_id: Annotated[str, Header(alias="X-Device-ID")] = "",
) -> BaseResponse[SessionResponse]:
    """Get session by ID endpoint — returns 404 if session doesn't belong to this device."""
    session = service.get_session(session_id, device_id=x_device_id)
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
    description="Update session title, metadata, or transition lifecycle status. Enforces device ownership.",
)
async def update_session(
    session_id: str,
    data: UpdateSessionRequest,
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
    x_device_id: Annotated[str, Header(alias="X-Device-ID")] = "",
) -> BaseResponse[SessionResponse]:
    """Update session endpoint — enforces device ownership before applying changes."""
    session = service.update_session(session_id, data, device_id=x_device_id)
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


@router.delete(
    "/{session_id}",
    response_model=BaseResponse[None],
    summary="Delete Research Session",
    description="Permanently delete a research session by ID. Enforces device ownership.",
)
async def delete_session(
    session_id: str,
    service: Annotated[SessionService, Depends(get_session_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
    x_device_id: Annotated[str, Header(alias="X-Device-ID")] = "",
) -> BaseResponse[None]:
    """Delete session endpoint — enforces device ownership before deletion."""
    service.delete_session(session_id, device_id=x_device_id)
    return BaseResponse(
        success=True,
        message="Research session deleted successfully.",
        request_id=request_id,
        data=None,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )


@router.get(
    "/{session_id}/messages",
    response_model=BaseResponse[ConversationMessagesListResponse],
    summary="List Conversation Messages",
    description="Retrieve all conversation messages for a session ordered by creation time.",
)
async def list_conversation_messages(
    session_id: str,
    service: Annotated[SessionService, Depends(get_session_service)],
    conversation_repo: Annotated[
        AbstractConversationRepository, Depends(get_conversation_repository_dep)
    ],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
    x_device_id: Annotated[str, Header(alias="X-Device-ID")] = "",
) -> BaseResponse[ConversationMessagesListResponse]:
    """List conversation messages — enforces session ownership before returning messages."""
    # Enforce session ownership (returns 404 if device mismatch)
    service.get_session(session_id, device_id=x_device_id)

    messages = conversation_repo.list_by_session(session_id)
    total = conversation_repo.count_by_session(session_id)

    message_responses = [
        ConversationMessageResponse(
            id=msg.id,
            session_id=msg.session_id,
            role=msg.role,
            content=msg.content,
            metadata=msg.metadata,
            created_at=msg.created_at,
        )
        for msg in messages
    ]

    return BaseResponse(
        success=True,
        message="Conversation messages retrieved successfully.",
        request_id=request_id,
        data=ConversationMessagesListResponse(
            messages=message_responses,
            total=total,
        ),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
