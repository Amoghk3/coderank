from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
@patch(
    "app.services.problem_service.ProblemService.get_problem",
    new_callable=AsyncMock,
)
async def test_get_problem(
    mock_service,
    client,
):
    mock_service.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "EASY",
        "statement": "Find two numbers that add up to target",
        "input_format": "Array of integers",
        "output_format": "Indices",
        "sample_input": "2 7 11 15\n9",
        "sample_output": "0 1",
        "time_limit_ms": 2000,
        "memory_limit_mb": 128,
    }

    response = await client.get(
        "/api/v1/problems/123"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["title"] == "Two Sum"
    assert body["slug"] == "two-sum"


@pytest.mark.asyncio
@patch(
    "app.services.problem_service.ProblemService.search_problems",
    new_callable=AsyncMock,
)
async def test_search_problems(
    mock_service,
    client,
):
    mock_service.return_value = []

    response = await client.get(
        "/api/v1/problems/search?q=two"
    )

    assert response.status_code == 200


@pytest.mark.asyncio
@patch(
    "app.services.problem_service.ProblemService.delete_problem",
    new_callable=AsyncMock,
)
async def test_delete_problem_forbidden(
    mock_service,
    client,
):
    response = await client.delete(
        "/api/v1/problems/123"
    )

    assert response.status_code in [
        401,
        403,
    ]