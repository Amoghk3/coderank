from uuid import UUID

from pydantic import BaseModel


class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = False
    points: int = 1


class TestCaseUpdate(BaseModel):
    input_data: str | None = None
    expected_output: str | None = None
    is_hidden: bool | None = None
    points: int | None = None


class TestCaseResponse(BaseModel):
    id: UUID

    problem_id: UUID

    input_data: str

    expected_output: str

    is_hidden: bool = False

    points: int

    model_config = {
        "from_attributes": True
    }