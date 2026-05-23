from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_case import TestCase


class TestCaseRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        test_case: TestCase,
    ):
        db.add(test_case)

        await db.commit()
        await db.refresh(test_case)

        return test_case

    @staticmethod
    async def get_by_problem(
        db: AsyncSession,
        problem_id: str,
    ):
        result = await db.execute(
            select(TestCase).where(
                TestCase.problem_id == problem_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        test_case_id: str,
    ):
        result = await db.execute(
            select(TestCase).where(
                TestCase.id == test_case_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        test_case: TestCase,
    ):
        await db.delete(test_case)
        await db.commit()