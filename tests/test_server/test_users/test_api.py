import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from app.db.models import User
from app.db.factories.user import DEFAULT_PASSWORD
from app.services.auth import decode_access_token
from app.api.users.rest import (
    USER_ALREADY_EXIST_MESSAGE,
    INCORRECT_CREDENTIALS_MESSAGE,
)
from app.server.server import app


@pytest.mark.asyncio
async def test_user_api_register(
    async_client: AsyncClient,
    builded_test_user: User,
):
    """Ensure that user can register."""
    response = await async_client.post(
        app.url_path_for("register"),
        json={
            "username": builded_test_user.username,
            "password": DEFAULT_PASSWORD,
            "email": builded_test_user.email,
        },
    )
    response_body = response.json()
    assert response.status_code == HTTP_201_CREATED, response_body
    assert response_body["username"] == builded_test_user.username
    assert response_body["email"] == builded_test_user.email
    assert isinstance(response_body["id"], int)
    assert response_body["created"]
    assert response_body["modified"]


@pytest.mark.asyncio
async def test_invalid_user_api_register(
    async_client: AsyncClient,
    test_user: User,
):
    """Ensure that user can't register with existing username and email."""
    response = await async_client.post(
        app.url_path_for("register"),
        json={
            "username": test_user.username,
            "password": DEFAULT_PASSWORD,
            "email": test_user.email,
        },
    )
    response_body = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST, response_body
    assert response.json()["detail"] == USER_ALREADY_EXIST_MESSAGE


@pytest.mark.asyncio
async def test_user_api_login(async_client: AsyncClient, test_user: User):
    """Ensure that user can login with credentials."""
    response = await async_client.post(
        app.url_path_for("login"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "password",
            "username": test_user.username,
            "password": DEFAULT_PASSWORD,
        },
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert response_body["token_type"] == "bearer"
    assert decode_access_token(
        response_body["access_token"],
    ) == test_user.username


@pytest.mark.asyncio
async def test_invalid_user_api_login_wrong_password(
    async_client: AsyncClient,
    test_user: User,
):
    """Ensure that user can't login with wrong password."""
    response = await async_client.post(
        app.url_path_for("login"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "password",
            "username": test_user.username,
            "password": "incorrect_password",
        },
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == INCORRECT_CREDENTIALS_MESSAGE


@pytest.mark.asyncio
async def test_invalid_user_api_login_nonexistent_user(
    async_client: AsyncClient,
):
    """Ensure that user can't login with non-existent username."""
    response = await async_client.post(
        app.url_path_for("login"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "password",
            "username": "non_existing_username",
            "password": DEFAULT_PASSWORD,
        },
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == INCORRECT_CREDENTIALS_MESSAGE
