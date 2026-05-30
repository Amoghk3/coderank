from pydantic import (
    BaseModel,
    Field,
)

from uuid import UUID

class ExecuteSubmissionRequest(
    BaseModel
):
    problem_id: UUID

    language_id: UUID

    source_code: str = Field(
        max_length=50000,
    )

    custom_input: str | None = None


class JudgeSubmissionRequest(
    BaseModel
):
    problem_id: UUID

    language_id: UUID

    source_code: str = Field(
        max_length=50000,
    )


class SubmissionResponse(
    BaseModel
):
    id: UUID

    user_id: UUID

    problem_id: UUID

    language_id: UUID

    custom_input: str | None

    status: str

    runtime_ms: int | None

    memory_kb: int | None

    class Config:
        from_attributes = True


class ExecutionResultResponse(
    BaseModel
):
    stdout: str | None

    stderr: str | None

    class Config:
        from_attributes = True


class JudgeCaseResultResponse(
    BaseModel
):
    expected_output: str

    actual_output: str

    passed: bool

    class Config:
        from_attributes = True


class SubmissionDetailResponse(
    BaseModel
):
    id: UUID

    status: str

    runtime_ms: int | None

    memory_kb: int | None

    execution_results: list[
        ExecutionResultResponse
    ] = []

    judge_case_results: list[
        JudgeCaseResultResponse
    ] = []

    class Config:
        from_attributes = True