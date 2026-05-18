from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class AuthRepository:

    @staticmethod
    async def create_refresh_token(
        db: AsyncSession,
        refresh_token: RefreshToken,
    ):
        db.add(refresh_token)

        await db.commit()
        await db.refresh(refresh_token)

        return refresh_token

    @staticmethod
    async def get_refresh_token(
        db: AsyncSession,
        token: str,
    ):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token == token
            )
        )

        return result.scalar_one_or_none()