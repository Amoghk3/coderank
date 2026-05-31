# tests/test_auth.py

from unittest.mock import AsyncMock, patch

import pytest

from httpx import ASGITransport
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client():

    transport = ASGITransport(
        app=app
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:

        yield ac


@pytest.mark.asyncio
@patch(
    "app.services.auth_service.AuthService.login",
    new_callable=AsyncMock,
)
async def test_login_success(
    mock_login,
    client,
):

    mock_login.return_value = {
        "access_token":
        "fake-token",

        "token_type":
        "bearer",
    }

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username":
            "admin@test.com",

            "password":
            "Admin123!",
        },
    )

    assert (
        response.status_code
        == 200
    )

    body = response.json()

    assert (
        body["access_token"]
        ==
        "fake-token"
    )


@pytest.mark.asyncio
@patch(
    "app.services.auth_service.AuthService.register",
    new_callable=AsyncMock,
)
async def test_register_success(
    mock_register,
    client,
):

    mock_register.return_value = {
        "id": "1",

        "email":
        "pytest@test.com",

        "username":
        "pytest",
    }

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email":
            "pytest@test.com",

            "username":
            "pytest",

            "password":
            "Password123!",
        },
    )

    assert (
        response.status_code
        == 200
    )


@pytest.mark.asyncio
@patch(
    "app.services.auth_service.AuthService.login",
    new_callable=AsyncMock,
)
async def test_login_failure(
    mock_login,
    client,
):

    from fastapi import (
        HTTPException,
    )

    mock_login.side_effect = (
        HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username":
            "admin@test.com",

            "password":
            "wrong",
        },
    )

    assert (
        response.status_code
        == 401
    )