from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger

from app.models.problem import Problem

from app.repositories.problem_repository import (
    ProblemRepository,
)

from app.schemas.problem_schema import (
    ProblemCreate,
    ProblemUpdate,
)
from app.models.enums import (
    ProblemDifficulty,
)


class ProblemService:

    @staticmethod
    async def create_problem(
        db: AsyncSession,
        payload: ProblemCreate,
    ):
        logger.info(
            f"Creating problem={payload.title}"
        )

        data = payload.model_dump()

        tags = data.pop(
            "tags",
            [],
        )

        problem = Problem(
            **data
        )

        problem = await ProblemRepository.create(
            db,
            problem,
        )

        await ProblemRepository.create_tags(
            db,
            problem.id,
            tags,
        )

        await db.commit()

        await db.refresh(problem)

        return problem

    @staticmethod
    async def get_problems(
        db: AsyncSession,
    ):
        return await ProblemRepository.get_all(
            db
        )

    @staticmethod
    async def get_problem(
        db: AsyncSession,
        problem_id: str,
    ):
        problem = await ProblemRepository.get_by_id(
            db,
            problem_id,
        )

        if not problem:
            raise HTTPException(
                status_code=404,
                detail="Problem not found",
            )

        return problem

    @staticmethod
    async def update_problem(
        db: AsyncSession,
        problem_id: str,
        payload: ProblemUpdate,
    ):
        problem = await ProblemRepository.get_by_id(
            db,
            problem_id,
        )

        if not problem:
            raise HTTPException(
                status_code=404,
                detail="Problem not found",
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(problem, key, value)

        await db.commit()
        await db.refresh(problem)

        return problem

    @staticmethod
    async def delete_problem(
        db: AsyncSession,
        problem_id: str,
    ):
        problem = await ProblemRepository.get_by_id(
            db,
            problem_id,
        )

        if not problem:
            raise HTTPException(
                status_code=404,
                detail="Problem not found",
            )

        await ProblemRepository.delete(
            db,
            problem,
        )

        return {
            "message": "Problem deleted successfully"
        }
    
 

    @staticmethod
    async def search_problems(
        db: AsyncSession,
        difficulty: ProblemDifficulty | None = None,
        tag: str | None = None,
        query: str | None = None,
    ):
        logger.info(
            f"Searching problems difficulty={difficulty} tag={tag} query={query}"
        )

        return await ProblemRepository.search_problems(
            db,
            difficulty,
            tag,
            query,
        )