from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


sync_database_url = settings.DATABASE_URL.replace(
    "asyncpg",
    "psycopg2",
)

engine = create_engine(
    sync_database_url,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)