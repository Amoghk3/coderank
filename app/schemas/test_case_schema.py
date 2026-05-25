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
    id: str
    problem_id: str
    input_data: str
    expected_output: str
    is_hidden: bool = False
    points: int

    class Config:
        from_attributes = True