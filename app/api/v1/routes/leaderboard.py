from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy import select, desc

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.leaderboard import Leaderboard
from app.models.user import User


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
        select(
            Leaderboard,
            User.email,
        )
        .join(
            User,
            Leaderboard.user_id == User.id,
        )
        .order_by(
            desc(
                Leaderboard.total_score
            )
        )
        .limit(100)
    )

    rows = result.all()

    leaderboard = []

    for rank, (lb, email) in enumerate(
        rows,
        start=1,
    ):
        leaderboard.append(
            {
                "rank": rank,
                "user_id": lb.user_id,
                "email": email,
                "accepted_count": lb.accepted_count,
                "total_submissions": lb.total_submissions,
                "total_score": lb.total_score,
                "best_runtime_ms": lb.best_runtime_ms,
                "updated_at": lb.updated_at,
            }
        )

    return leaderboard