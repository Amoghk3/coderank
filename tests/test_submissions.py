from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_submission_history_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/submissions/history"
    )

    assert response.status_code in [
        401,
        403,
    ]


@pytest.mark.asyncio
async def test_judge_requires_auth(
    client,
):
    response = await client.post(
        "/api/v1/submissions/judge",
        json={},
    )

    assert response.status_code in [
        401,
        403,
        422,
    ]


@pytest.mark.asyncio
async def test_execute_requires_auth(
    client,
):
    response = await client.post(
        "/api/v1/submissions/execute",
        json={},
    )

    assert response.status_code in [
        401,
        403,
        422,
    ]


@pytest.mark.asyncio
async def test_submission_detail_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/submissions/123"
    )

    assert response.status_code in [
        401,
        403,
    ]


@pytest.mark.asyncio
async def test_submission_results_requires_auth(
    client,
):
    response = await client.get(
        "/api/v1/submissions/123/results"
    )

    assert response.status_code in [
        401,
        403,
    ]