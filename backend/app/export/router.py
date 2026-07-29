"""API router for Report Export endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from app.core.repositories.session import AbstractSessionRepository
from app.dependencies import get_session_repository_dep
from app.export.service import ReportExportService

router = APIRouter(tags=["Reports"])


def get_export_service(
    session_repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
) -> ReportExportService:
    """Dependency provider creating ReportExportService instance."""
    return ReportExportService(session_repository=session_repo)


@router.get(
    "/{session_id}/export",
    summary="Export Research Report",
    description="Export a completed research report in Markdown (.md) or PDF (.pdf) format.",
    response_class=Response,
)
async def export_report_endpoint(
    session_id: str,
    service: Annotated[ReportExportService, Depends(get_export_service)],
    format: Annotated[
        str,
        Query(
            description="Export file format: 'markdown' or 'pdf'",
        ),
    ] = "markdown",
) -> Response:
    """Export completed research report as downloadable file."""
    result = service.export_report(session_id=session_id, format_str=format)
    return Response(
        content=result.content,
        media_type=result.media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{result.filename}"'
        },
    )
