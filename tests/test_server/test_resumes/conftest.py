import pytest_asyncio

from app.db.models import User, Resume
from app.db.factories import AsyncResumeFactory
from app.services.resume_upgrade import PERMISSIBLE_CONTENT_LEN


@pytest_asyncio.fixture(scope="module")
async def multiple_resumes_for_test_user(test_user: User) -> list[Resume]:
    """Return 3 Resume instance related to test_user for tests."""
    return await AsyncResumeFactory.create_batch(size=3, user=test_user)


@pytest_asyncio.fixture(scope="function")
async def resume_for_test_user(test_user: User) -> Resume:
    """Return Resume instance related to test_user for tests."""
    return await AsyncResumeFactory.create(user=test_user)


@pytest_asyncio.fixture(scope="module")
async def builded_resume_for_test_user(test_user: User) -> Resume:
    """Return builded Resume instance related to test_user for tests."""
    return await AsyncResumeFactory.build(user=test_user)


@pytest_asyncio.fixture(scope="function")
async def resume_with_too_long_content(test_user: User) -> Resume:
    """Return Resume instance with too long content that can't be improved."""
    return await AsyncResumeFactory.create(
        user=test_user,
        content="*" * (PERMISSIBLE_CONTENT_LEN + 1),
    )
