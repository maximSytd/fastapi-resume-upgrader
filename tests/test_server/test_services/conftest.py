import pytest

from app.services.resume_upgrade import PERMISSIBLE_CONTENT_LEN

@pytest.fixture(scope="module")
def dummy_resume_content() -> str:
    """Return dummy resume content for tests."""
    return "*" * (PERMISSIBLE_CONTENT_LEN)


@pytest.fixture(scope="module")
def too_long_resume_content() -> str:
    """Return resume content exceeding the maximum length."""
    return "*" * (PERMISSIBLE_CONTENT_LEN + 1)
