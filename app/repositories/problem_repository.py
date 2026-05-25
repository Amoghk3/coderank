from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.problem import Problem

from sqlalchemy import select

from app.models.problem import Problem
from app.models.problem_tag import ProblemTag



class ProblemRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        problem: Problem,
    ):
        db.add(problem)

        await db.commit()
        await db.refresh(problem)

        return problem

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Problem)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        problem_id: str,
    ):
        result = await db.execute(
            select(Problem).where(
                Problem.id == problem_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        problem: Problem,
    ):
        await db.delete(problem)
        await db.commit()


    @staticmethod
    async def search_problems(
        db,
        difficulty: str | None = None,
        tag: str | None = None,
        query: str | None = None,
    ):

        stmt = select(Problem)

        if difficulty:

            stmt = stmt.where(
                Problem.difficulty
                == difficulty
            )

        if query:

            stmt = stmt.where(
                Problem.title.ilike(
                    f"%{query}%"
                )
            )

        if tag:

            stmt = (
                stmt.join(ProblemTag)
                .where(
                    ProblemTag.tag == tag
                )
            )

        result = await db.execute(stmt)

        return result.scalars().all()