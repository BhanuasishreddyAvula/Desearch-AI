"""Report Export Service coordinating deterministic report formatting."""

from app.core.exceptions import ResourceNotFoundException, ValidationException
from app.core.repositories.session import AbstractSessionRepository
from app.export.enums import ExportFormat
from app.export.exceptions import ReportNotExportableException
from app.export.formatters.markdown import MarkdownExportFormatter
from app.export.formatters.pdf import PdfExportFormatter
from app.export.models import ExportResult
from app.observability.logger import get_app_logger
from app.sessions.enums import SessionStatus

logger = get_app_logger("export.service")


class ReportExportService:
    """Service retrieving canonical completed report and formatting downloadable exports."""

    def __init__(self, session_repository: AbstractSessionRepository) -> None:
        self.session_repository = session_repository

    def export_report(self, session_id: str, format_str: str) -> ExportResult:
        """Retrieve completed report by session_id and generate requested format export."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            logger.error("Export Failed | Session '%s' not found", session_id)
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )

        report_data = session.metadata.get("report_result")
        if not report_data or session.status != SessionStatus.COMPLETED:
            logger.error("Export Failed | Session '%s' report not completed/exportable", session_id)
            raise ReportNotExportableException(
                message=f"Research report for session '{session_id}' is not completed or exportable."
            )

        try:
            export_format = ExportFormat.from_str(format_str)
        except ValueError as exc:
            logger.error("Export Failed | Unsupported format '%s'", format_str)
            raise ValidationException(
                message=f"Unsupported export format '{format_str}'. Supported formats are 'markdown' and 'pdf'."
            ) from exc

        if export_format == ExportFormat.MARKDOWN:
            formatter = MarkdownExportFormatter()
        elif export_format == ExportFormat.PDF:
            formatter = PdfExportFormatter()
        else:
            raise ValidationException(
                message=f"Unsupported export format '{format_str}'."
            )

        result = formatter.format_report(report_data, session_id)

        logger.info(
            "Report Exported | Session: %s | Format: %s | Filename: %s | Size: %d bytes",
            session_id,
            export_format.value,
            result.filename,
            len(result.content),
        )

        return result
