from db.models import Resume

CONTENT_UPGRADE_AI_STUB = " [improved]"
PERMISSIBLE_CONTENT_LEN = Resume.CONTENT_MAX_LEN - 1 - len(
    CONTENT_UPGRADE_AI_STUB,
)
RESUME_CONTENT_LENGTH_ERROR_MESSAGE = (
    f"Resume is longer than {PERMISSIBLE_CONTENT_LEN}, so it can't be upgraded"
)


class ResumeContentLengthError(Exception):
    """Resume error for too long content."""


def improve_resume_content(content: str) -> str:
    """Return and improve resume content."""
    if len(
        content,
    ) >= Resume.CONTENT_MAX_LEN - len(
        CONTENT_UPGRADE_AI_STUB,
    ):
        raise ResumeContentLengthError(RESUME_CONTENT_LENGTH_ERROR_MESSAGE)
    content += CONTENT_UPGRADE_AI_STUB
    return content
