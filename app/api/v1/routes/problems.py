from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user

from app.core.database import get_db

from app.models.user import User

from app.schemas.problem_schema import (
    ProblemCreate,
    ProblemUpdate,
    ProblemResponse,
)

from app.services.problem_service import (
    ProblemService,
)


router = APIRouter(
    prefix="/problems",
    tags=["Problems"],
)


@router.post(
    "",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_problem(
    payload: ProblemCreate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await ProblemService.create_problem(
        db,
        payload,
    )


@router.get(
    "",
    response_model=list[ProblemResponse],
)
async def get_problems(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await ProblemService.get_problems(
        db,
    )


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse,
)
async def get_problem(
    problem_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await ProblemService.get_problem(
        db,
        problem_id,
    )


@router.put(
    "/{problem_id}",
    response_model=ProblemResponse,
)
async def update_problem(
    problem_id: str,
    payload: ProblemUpdate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await ProblemService.update_problem(
        db,
        problem_id,
        payload,
    )


@router.delete(
    "/{problem_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_problem(
    problem_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await ProblemService.delete_problem(
        db,
        problem_id,
    )