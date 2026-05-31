import sys
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as ac:
        yield ac


@pytest.fixture
def mock_user_id():
    return "e76c7eaa-4371-47b2-9fff-52eb5a552192"


@pytest.fixture
def mock_problem_id():
    return "ebd6d3ed-5636-486e-9c77-c168d4a1b4a9"


@pytest.fixture
def mock_language_id():
    return "6bfb9186-baa4-4113-8b1f-a80b181fb9f9"