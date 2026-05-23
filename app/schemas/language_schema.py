from pydantic import BaseModel


class LanguageCreate(BaseModel):
    name: str
    version: str
    docker_image: str
    compile_command: str | None = None
    run_command: str
    time_limit: int = 2
    memory_limit: int = 256


class LanguageUpdate(BaseModel):
    version: str | None = None
    docker_image: str | None = None
    compile_command: str | None = None
    run_command: str | None = None
    time_limit: int | None = None
    memory_limit: int | None = None
    is_active: bool | None = None


class LanguageResponse(BaseModel):
    id: str
    name: str
    version: str
    docker_image: str
    compile_command: str | None
    run_command: str
    time_limit: int
    memory_limit: int
    is_active: bool

    class Config:
        from_attributes = True