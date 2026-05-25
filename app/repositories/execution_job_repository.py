from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.execution_job import (
    ExecutionJob,
)


class ExecutionJobRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        execution_job: ExecutionJob,
    ):
        db.add(execution_job)

        await db.commit()
        await db.refresh(execution_job)

        return execution_job

    @staticmethod
    async def get_by_submission(
        db: AsyncSession,
        submission_id: str,
    ):
        result = await db.execute(
            select(ExecutionJob).where(
                ExecutionJob.submission_id
                == submission_id
            )
        )

        return result.scalars().all()