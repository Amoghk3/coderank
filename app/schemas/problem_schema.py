from pydantic import BaseModel


class ProblemCreate(BaseModel):
    title: str
    slug: str
    difficulty: str
    statement: str
    input_format: str
    output_format: str
    constraints: str
    sample_input: str
    sample_output: str
    time_limit: int = 2
    memory_limit: int = 256
    difficulty: str
    time_limit_ms: int = 2000
    memory_limit_mb: int = 128

    constraints: str | None = None
    examples: str | None = None

    tags: list[str] = []


class ProblemUpdate(BaseModel):
    title: str | None = None
    difficulty: str | None = None
    statement: str | None = None
    input_format: str | None = None
    output_format: str | None = None
    constraints: str | None = None
    sample_input: str | None = None
    sample_output: str | None = None
    time_limit: int | None = None
    memory_limit: int | None = None
    difficulty: str
    time_limit_ms: int = 2000
    memory_limit_mb: int = 128

    constraints: str | None = None
    examples: str | None = None

    tags: list[str] = []


class ProblemResponse(BaseModel):
    id: str
    title: str
    slug: str
    difficulty: str
    statement: str
    input_format: str
    output_format: str
    constraints: str
    sample_input: str
    sample_output: str
    time_limit: int
    memory_limit: int

    class Config:
        from_attributes = True