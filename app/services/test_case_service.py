from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger

from app.models.test_case import TestCase

from app.repositories.problem_repository import (
    ProblemRepository,
)

from app.repositories.test_case_repository import (
    TestCaseRepository,
)

from app.schemas.test_case_schema import (
    TestCaseCreate,
    TestCaseUpdate,
)


class TestCaseService:

    @staticmethod
    async def create_test_case(
        db: AsyncSession,
        problem_id: str,
        payload: TestCaseCreate,
    ):
        logger.info(
            f"Creating test case for problem={problem_id}"
        )

        problem = await ProblemRepository.get_by_id(
            db,
            problem_id,
        )

        if not problem:
            raise HTTPException(
                status_code=404,
                detail="Problem not found",
            )

        test_case = TestCase(
            problem_id=problem.id,
            **payload.model_dump(),
        )

        return await TestCaseRepository.create(
            db,
            test_case,
        )

    @staticmethod
    async def get_test_cases(
        db: AsyncSession,
        problem_id: str,
    ):
        return await TestCaseRepository.get_by_problem(
            db,
            problem_id,
        )

    @staticmethod
    async def get_test_case(
        db: AsyncSession,
        test_case_id: str,
    ):
        test_case = await TestCaseRepository.get_by_id(
            db,
            test_case_id,
        )

        if not test_case:
            raise HTTPException(
                status_code=404,
                detail="Test case not found",
            )

        return test_case

    @staticmethod
    async def update_test_case(
        db: AsyncSession,
        test_case_id: str,
        payload: TestCaseUpdate,
    ):
        test_case = await TestCaseRepository.get_by_id(
            db,
            test_case_id,
        )

        if not test_case:
            raise HTTPException(
                status_code=404,
                detail="Test case not found",
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(test_case, key, value)

        await db.commit()
        await db.refresh(test_case)

        return test_case

    @staticmethod
    async def delete_test_case(
        db: AsyncSession,
        test_case_id: str,
    ):
        test_case = await TestCaseRepository.get_by_id(
            db,
            test_case_id,
        )

        if not test_case:
            raise HTTPException(
                status_code=404,
                detail="Test case not found",
            )

        await TestCaseRepository.delete(
            db,
            test_case,
        )

        return {
            "message": "Test case deleted successfully"
        }