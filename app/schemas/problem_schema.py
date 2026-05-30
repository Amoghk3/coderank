from uuid import UUID

from pydantic import BaseModel


class ProblemCreate(BaseModel):
    title: str
    slug: str

    difficulty: str

    statement: str

    input_format: str
    output_format: str

    sample_input: str
    sample_output: str

    time_limit_ms: int = 2000
    memory_limit_mb: int = 128

    constraints: str | None = None
    examples: str | None = None

    tags: list[str] = []


class ProblemUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None

    difficulty: str | None = None

    statement: str | None = None

    input_format: str | None = None
    output_format: str | None = None

    sample_input: str | None = None
    sample_output: str | None = None

    time_limit_ms: int | None = None
    memory_limit_mb: int | None = None

    constraints: str | None = None
    examples: str | None = None

    tags: list[str] | None = None


class ProblemResponse(BaseModel):
    id: UUID

    title: str
    slug: str

    difficulty: str

    statement: str

    input_format: str
    output_format: str

    sample_input: str
    sample_output: str

    time_limit_ms: int
    memory_limit_mb: int

    constraints: str | None = None
    examples: str | None = None

    model_config = {
        "from_attributes": True
    }