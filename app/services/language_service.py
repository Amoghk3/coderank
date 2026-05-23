from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger

from app.models.language import Language

from app.repositories.language_repository import (
    LanguageRepository,
)

from app.schemas.language_schema import (
    LanguageCreate,
    LanguageUpdate,
)


class LanguageService:

    @staticmethod
    async def create_language(
        db: AsyncSession,
        payload: LanguageCreate,
    ):
        logger.info(
            f"Creating language={payload.name}"
        )

        language = Language(
            **payload.model_dump()
        )

        return await LanguageRepository.create(
            db,
            language,
        )

    @staticmethod
    async def get_languages(
        db: AsyncSession,
    ):
        return await LanguageRepository.get_all(
            db
        )

    @staticmethod
    async def get_language(
        db: AsyncSession,
        language_id: str,
    ):
        language = await LanguageRepository.get_by_id(
            db,
            language_id,
        )

        if not language:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        return language

    @staticmethod
    async def update_language(
        db: AsyncSession,
        language_id: str,
        payload: LanguageUpdate,
    ):
        language = await LanguageRepository.get_by_id(
            db,
            language_id,
        )

        if not language:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(language, key, value)

        await db.commit()
        await db.refresh(language)

        return language

    @staticmethod
    async def delete_language(
        db: AsyncSession,
        language_id: str,
    ):
        language = await LanguageRepository.get_by_id(
            db,
            language_id,
        )

        if not language:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        await LanguageRepository.delete(
            db,
            language,
        )

        return {
            "message": "Language deleted successfully"
        }