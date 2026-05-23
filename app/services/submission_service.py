from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger

from app.models.submission import Submission

from app.models.enums import (
    SubmissionStatus,
)

from app.models.user import User

from app.repositories.problem_repository import (
    ProblemRepository,
)

from app.repositories.language_repository import (
    LanguageRepository,
)

from app.repositories.submission_repository import (
    SubmissionRepository,
)

from app.schemas.submission_schema import (
    ExecuteSubmissionRequest,
    JudgeSubmissionRequest,
)

from app.workers.execution_worker import (
    execute_submission_task,
)


class SubmissionService:

    @staticmethod
    async def execute_submission(
        db: AsyncSession,
        payload: ExecuteSubmissionRequest,
        current_user: User,
    ):
        logger.info(
            f"Execute submission user={current_user.id}"
        )

        problem = await ProblemRepository.get_by_id(
            db,
            payload.problem_id,
        )

        if not problem:
            raise HTTPException(
                status_code=404,
                detail="Problem not found",
            )

        language = await LanguageRepository.get_by_id(
            db,
            payload.language_id,
        )

        if not language:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        submission = Submission(
            user_id=current_user.id,
            problem_id=payload.problem_id,
            language_id=payload.language_id,
            source_code=payload.source_code,
            custom_input=payload.custom_input,
            status=SubmissionStatus.PENDING,
        )

        submission = await SubmissionRepository.create(
            db,
            submission,
        )

        execute_submission_task.delay(
            str(submission.id)
        )

        return submission

    @staticmethod
    async def judge_submission(
        db: AsyncSession,
        payload: JudgeSubmissionRequest,
        current_user: User,
    ):
        logger.info(
            f"Judge submission user={current_user.id}"
        )

        problem = await ProblemRepository.get_by_id(
            db,
            payload.problem_id,
        )

        if not problem:
            raise HTTPException(
                status_code=404,
                detail="Problem not found",
            )

        language = await LanguageRepository.get_by_id(
            db,
            payload.language_id,
        )

        if not language:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        submission = Submission(
            user_id=current_user.id,
            problem_id=payload.problem_id,
            language_id=payload.language_id,
            source_code=payload.source_code,
            status=SubmissionStatus.PENDING,
        )

        submission = await SubmissionRepository.create(
            db,
            submission,
        )

        execute_submission_task.delay(
            str(submission.id)
        )

        return submission

    @staticmethod
    async def get_submission(
        db: AsyncSession,
        submission_id: str,
    ):
        submission = (
            await SubmissionRepository.get_by_id(
                db,
                submission_id,
            )
        )

        if not submission:
            raise HTTPException(
                status_code=404,
                detail="Submission not found",
            )

        return submission

    @staticmethod
    async def get_submission_history(
        db: AsyncSession,
        current_user: User,
    ):
        return (
            await SubmissionRepository.get_user_submissions(
                db,
                str(current_user.id),
            )
        )