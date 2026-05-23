from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.language import Language


class LanguageRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        language: Language,
    ):
        db.add(language)

        await db.commit()
        await db.refresh(language)

        return language

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Language)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        language_id: str,
    ):
        result = await db.execute(
            select(Language).where(
                Language.id == language_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        language: Language,
    ):
        await db.delete(language)
        await db.commit()