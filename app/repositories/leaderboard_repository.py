from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leaderboard import (
    Leaderboard,
)


class LeaderboardRepository:

    @staticmethod
    async def get_by_user_id(
        db: AsyncSession,
        user_id: str,
    ):
        result = await db.execute(
            select(Leaderboard).where(
                Leaderboard.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db: AsyncSession,
        leaderboard: Leaderboard,
    ):
        db.add(leaderboard)

        await db.commit()
        await db.refresh(leaderboard)

        return leaderboard

    @staticmethod
    async def update(
        db: AsyncSession,
        leaderboard: Leaderboard,
    ):
        await db.commit()
        await db.refresh(leaderboard)

        return leaderboard