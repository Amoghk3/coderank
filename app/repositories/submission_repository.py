from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.submission import Submission
from sqlalchemy.orm import (
    selectinload,
)


class SubmissionRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        submission: Submission,
    ):
        db.add(submission)

        await db.commit()
        await db.refresh(submission)

        return submission

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        submission_id: str,
    ):
        result = await db.execute(
            select(Submission).where(
                Submission.id == submission_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_submissions(
        db: AsyncSession,
        user_id: str,
    ):
        result = await db.execute(
            select(Submission).where(
                Submission.user_id == user_id
            )
        )

        return result.scalars().all()
    
    @staticmethod
    async def update(
        db: AsyncSession,
        submission: Submission,
    ):
        await db.commit()
        await db.refresh(submission)

        return submission
    
    @staticmethod
    async def get_submission_detail(
        db: AsyncSession,
        submission_id: str,
    ):

        result = await db.execute(
            select(Submission)
            .where(
                Submission.id == submission_id
            )
            .options(
                selectinload(
                    Submission.execution_results
                ),

                selectinload(
                    Submission.judge_case_results
                ),
            )
        )

        return result.scalar_one_or_none()