import pytest


@pytest.mark.asyncio
async def test_get_test_cases_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/problems/123/test-cases"
    )

    assert response.status_code in [
        401,
        403,
    ]


@pytest.mark.asyncio
async def test_get_single_test_case_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/test-cases/123"
    )

    assert response.status_code in [
        401,
        403,
    ]


@pytest.mark.asyncio
async def test_create_test_case_requires_admin(
    client,
):
    response = await client.post(
        "/api/v1/problems/123/test-cases",
        json={},
    )

    assert response.status_code in [
        401,
        403,
    ]