import datetime

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from app.db.models import Resume
from app.api.resumes.rest import RESUME_NOT_FOUND_MESSAGE
from app.server.server import app
from app.services.resume_upgrade import RESUME_CONTENT_LENGTH_ERROR_MESSAGE


@pytest.mark.asyncio
async def test_resume_api_list(
    authorized_async_client: AsyncClient,
    multiple_resumes_for_test_user: list[Resume],
):
    """Ensure that user can get list of resumes."""
    response = await authorized_async_client.get(
        app.url_path_for("list_resumes"),
        params={
            "page": 1,
            "size": 50,
        },
        follow_redirects=True,
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert len(response_body["items"]) == len(multiple_resumes_for_test_user)


@pytest.mark.asyncio
async def test_resume_api_create(
    authorized_async_client: AsyncClient,
    builded_resume_for_test_user: Resume,
):
    """Ensure that authenticated user can create resume."""
    response = await authorized_async_client.post(
        app.url_path_for("create_resume"),
        json={
            "title": builded_resume_for_test_user.title,
            "content": builded_resume_for_test_user.content,
        },
        follow_redirects=True,
    )
    response_body = response.json()
    assert response.status_code == HTTP_201_CREATED, response_body
    assert response_body["id"]
    assert response_body["title"] == builded_resume_for_test_user.title
    assert response_body["content"] == builded_resume_for_test_user.content
    assert response_body["created"]
    assert response_body["modified"]


@pytest.mark.asyncio
async def test_resume_api_get(
    authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
):
    """Ensure that authenticated user can get resume by id."""
    response = await authorized_async_client.get(
        app.url_path_for("get_resume", resume_id=resume_for_test_user.id),
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert response_body["id"]
    assert response_body["title"] == resume_for_test_user.title
    assert response_body["content"] == resume_for_test_user.content
    assert datetime.datetime.fromisoformat(
        response_body["created"].replace(
            "Z",
            "+00:00",
            ),
        ) == resume_for_test_user.created
    assert datetime.datetime.fromisoformat(
        response_body["modified"].replace(
            "Z",
            "+00:00",
            ),
        ) == resume_for_test_user.modified


@pytest.mark.asyncio
async def test_resume_api_update(
    authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
    builded_resume_for_test_user: Resume,
):
    """Ensure that authenticated user can update resume by id."""
    response = await authorized_async_client.put(
        app.url_path_for("update_resume", resume_id=resume_for_test_user.id),
        json={
            "title": builded_resume_for_test_user.title,
            "content": builded_resume_for_test_user.content,
        },
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert response_body["id"]
    assert response_body["title"] == builded_resume_for_test_user.title
    assert response_body["content"] == builded_resume_for_test_user.content
    assert datetime.datetime.fromisoformat(
        response_body["created"].replace(
            "Z",
            "+00:00",
            ),
        ) == resume_for_test_user.created
    assert response_body["modified"]

@pytest.mark.asyncio
async def test_resume_api_delete(
    authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
):
    """Ensure that authenticated user can delete resume by id."""
    response = await authorized_async_client.delete(
        app.url_path_for("delete_resume", resume_id=resume_for_test_user.id),
        follow_redirects=True,
    )
    assert response.status_code == HTTP_204_NO_CONTENT
    assert resume_for_test_user._saved_in_db
    assert await Resume.get_or_none(id=resume_for_test_user.id) is None


@pytest.mark.asyncio
async def test_resume_api_improve(
    authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
):
    """Ensure that user can improve resume by id."""
    await resume_for_test_user.save()
    response = await authorized_async_client.post(
        app.url_path_for(
            "improve_resume",
            resume_id=resume_for_test_user.id,
        ),
    )
    assert response.status_code == HTTP_200_OK, response.json()


@pytest.mark.asyncio
async def test_invalid_resume_api_improve(
    authorized_async_client: AsyncClient,
    resume_with_too_long_content: Resume,
):
    """Ensure that user can't improve resume with large content by id."""
    response = await authorized_async_client.post(
        app.url_path_for(
            "improve_resume",
            resume_id=resume_with_too_long_content.id,
        ),
    )
    response_body = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST, response_body
    assert response_body["detail"] == RESUME_CONTENT_LENGTH_ERROR_MESSAGE


@pytest.mark.asyncio
async def test_access_control_task_api_get(
    unfair_authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
):
    """Ensure that api have restrict access for get other user resumes."""
    response = await unfair_authorized_async_client.get(
        app.url_path_for(
            "get_resume",
            resume_id=resume_for_test_user.id,
        ),
    )
    response_body = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response_body["detail"] == RESUME_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_access_control_task_api_update(
    unfair_authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
):
    """Ensure that api have restrict access for update other user resumes."""
    response = await unfair_authorized_async_client.put(
        app.url_path_for(
            "update_resume",
            resume_id=resume_for_test_user.id,
        ),
        json={
            "title": "some title",
            "content": "some content",
        }
    )
    response_body = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response_body["detail"] == RESUME_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_access_control_task_api_delete(
    unfair_authorized_async_client: AsyncClient,
    resume_for_test_user: Resume,
):
    """Ensure that api have restrict access for delete other user resumes."""
    response = await unfair_authorized_async_client.delete(
        app.url_path_for(
            "delete_resume",
            resume_id=resume_for_test_user.id,
        ),
    )
    response_body = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response_body["detail"] == RESUME_NOT_FOUND_MESSAGE
