from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_user,
    require_roles,
)

from app.core.database import get_db

from app.models.enums import (
    UserRole,
)

from app.models.user import User

from app.schemas.problem_schema import (
    ProblemCreate,
    ProblemUpdate,
    ProblemResponse,
)

from app.services.problem_service import (
    ProblemService,
)
from app.models.enums import (
    ProblemDifficulty,
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

    current_user: Annotated[
        User,
        Depends(
            require_roles(
                [
                    UserRole.ADMIN,
                    UserRole.MODERATOR,
                ]
            )
        ),
    ],

    db: Annotated[
        AsyncSession,
        Depends(get_db),
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
):
    return await ProblemService.get_problems(
        db,
    )



@router.get("/search")
async def search_problems(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],

    difficulty: ProblemDifficulty | None = None,

    tag: str | None = None,

    q: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
):
    return await ProblemService.search_problems(
        db,
        difficulty,
        tag,
        q,
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

    current_user: Annotated[
        User,
        Depends(
            require_roles(
                [
                    UserRole.ADMIN,
                    UserRole.MODERATOR,
                ]
            )
        ),
    ],

    db: Annotated[
        AsyncSession,
        Depends(get_db),
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

    current_user: Annotated[
        User,
        Depends(
            require_roles(
                [
                    UserRole.ADMIN,
                ]
            )
        ),
    ],

    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    return await ProblemService.delete_problem(
        db,
        problem_id,
    )

