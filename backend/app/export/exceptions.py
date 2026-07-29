"""Export domain exception definitions."""

from app.core.exceptions import AppException, ValidationException


class ExportException(AppException):
    """Base exception for report export operation failures."""

    def __init__(
        self,
        message: str = "Report export operation failed",
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message, error_code="EXPORT_ERROR", details=details
        )


class ReportNotExportableException(ValidationException):
    """Raised when attempting to export a report that is not yet completed or exportable."""

    def __init__(
        self,
        message: str = "Report is not completed or exportable",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)
