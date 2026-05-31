from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
@patch("sqlalchemy.ext.asyncio.AsyncSession.execute", new_callable=AsyncMock)
async def test_get_leaderboard_success(
    mock_execute,
    client,
):
    lb = MagicMock()

    lb.user_id = "user-1"
    lb.accepted_count = 5
    lb.total_submissions = 10
    lb.total_score = 500
    lb.best_runtime_ms = 120
    lb.updated_at = "2026-05-30"

    result = MagicMock()

    result.all.return_value = [
        (lb, "admin@test.com")
    ]

    mock_execute.return_value = result

    response = await client.get(
        "/api/v1/leaderboard"
    )

    assert response.status_code == 200


@pytest.mark.asyncio
@patch("sqlalchemy.ext.asyncio.AsyncSession.execute", new_callable=AsyncMock)
async def test_get_leaderboard_empty(
    mock_execute,
    client,
):
    result = MagicMock()

    result.all.return_value = []

    mock_execute.return_value = result

    response = await client.get(
        "/api/v1/leaderboard"
    )

    assert response.status_code == 200

    assert response.json() == []