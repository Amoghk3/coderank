import pytest


@pytest.mark.asyncio
async def test_languages_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/languages"
    )

    assert response.status_code in [
        401,
        403,
    ]


@pytest.mark.asyncio
async def test_language_by_id_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/languages/123"
    )

    assert response.status_code in [
        401,
        403,
    ]


@pytest.mark.asyncio
async def test_create_language_requires_admin(
    client,
):
    response = await client.post(
        "/api/v1/languages",
        json={},
    )

    assert response.status_code in [
        401,
        403,
    ]