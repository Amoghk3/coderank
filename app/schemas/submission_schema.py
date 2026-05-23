from pydantic import BaseModel


class ExecuteSubmissionRequest(BaseModel):
    problem_id: str
    language_id: str
    source_code: str
    custom_input: str


class JudgeSubmissionRequest(BaseModel):
    problem_id: str
    language_id: str
    source_code: str


class SubmissionResponse(BaseModel):
    id: str
    user_id: str
    problem_id: str
    language_id: str
    source_code: str
    custom_input: str | None
    status: str
    runtime_ms: int | None
    memory_kb: int | None

    class Config:
        from_attributes = True