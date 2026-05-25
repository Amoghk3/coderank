from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_user,
)

from app.core.database import get_db

from app.core.rate_limit import (
    limiter,
)

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
@limiter.limit("20/minute")
async def execute_submission(
    request: Request,

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
@limiter.limit("5/minute")
async def judge_submission(
    request: Request,

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


@router.get("/{submission_id}")
async def get_submission(
    submission_id: str,

    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],

    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):

    return await SubmissionService.get_submission(
        db,
        submission_id,
        current_user,
    )


@router.get("/{submission_id}/results")
async def get_submission_results(
    submission_id: str,

    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],

    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):

    return await SubmissionService.get_submission_results(
        db,
        submission_id,
        current_user,
    )