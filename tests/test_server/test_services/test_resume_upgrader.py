import pytest

from app.services.resume_upgrade import (
    RESUME_CONTENT_LENGTH_ERROR_MESSAGE,
    CONTENT_UPGRADE_AI_STUB,
    ResumeContentLengthError,
    improve_resume_content,
)


def test_improve_resume(dummy_resume_content: str):
    """Check for proper functionality of resume improve."""
    previous_content = dummy_resume_content
    new_content = improve_resume_content(dummy_resume_content)
    assert previous_content in new_content
    assert CONTENT_UPGRADE_AI_STUB in new_content


def test_invalid_improve_resume(too_long_resume_content: str):
    """Ensure that resume improve raise error with incorrect content."""
    with pytest.raises(ResumeContentLengthError) as exc_info:
        improve_resume_content(too_long_resume_content)
    assert RESUME_CONTENT_LENGTH_ERROR_MESSAGE in str(exc_info.value)
