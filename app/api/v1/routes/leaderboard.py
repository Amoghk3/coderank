from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy import desc

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.leaderboard import (
    Leaderboard,
)


router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"],
)


@router.get("")
async def get_leaderboard(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):

    result = await db.execute(
        Leaderboard.__table__
        .select()
        .order_by(
            desc(
                Leaderboard.total_score
            )
        )
        .limit(100)
    )

    return result.mappings().all()