from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user

from app.core.database import get_db

from app.models.user import User

from app.schemas.submission_schema import (
    ExecuteSubmissionRequest,
    JudgeSubmissionRequest,
    SubmissionResponse,
)

from app.services.submission_service import (
    SubmissionService,
)


router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "/execute",
    response_model=SubmissionResponse,
)
async def execute_submission(
    payload: ExecuteSubmissionRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await SubmissionService.execute_submission(
        db,
        payload,
        current_user,
    )


@router.post(
    "/judge",
    response_model=SubmissionResponse,
)
async def judge_submission(
    payload: JudgeSubmissionRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await SubmissionService.judge_submission(
        db,
        payload,
        current_user,
    )


@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse,
)
async def get_submission(
    submission_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    return await SubmissionService.get_submission(
        db,
        submission_id,
    )


@router.get(
    "/history",
    response_model=list[SubmissionResponse],
)
async def get_submission_history(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await SubmissionService.get_submission_history(
        db,
        current_user,
    )