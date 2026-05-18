from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CodeRank"

    DATABASE_URL: str
    REDIS_URL: str

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"


settings = Settings()