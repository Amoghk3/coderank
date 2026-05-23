from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_user,
    role_required,
)

from app.core.database import get_db

from app.models.enums import UserRole
from app.models.user import User

from app.schemas.test_case_schema import (
    TestCaseCreate,
    TestCaseUpdate,
    TestCaseResponse,
)

from app.services.test_case_service import (
    TestCaseService,
)


router = APIRouter(
    tags=["Test Cases"],
)


@router.post(
    "/problems/{problem_id}/test-cases",
    response_model=TestCaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_test_case(
    problem_id: str,
    payload: TestCaseCreate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(
            role_required(
                [UserRole.ADMIN]
            )
        ),
    ],
):
    return await TestCaseService.create_test_case(
        db,
        problem_id,
        payload,
    )


@router.get(
    "/problems/{problem_id}/test-cases",
    response_model=list[TestCaseResponse],
)
async def get_test_cases(
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
    return await TestCaseService.get_test_cases(
        db,
        problem_id,
    )


@router.get(
    "/test-cases/{test_case_id}",
    response_model=TestCaseResponse,
)
async def get_test_case(
    test_case_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await TestCaseService.get_test_case(
        db,
        test_case_id,
    )


@router.put(
    "/test-cases/{test_case_id}",
    response_model=TestCaseResponse,
)
async def update_test_case(
    test_case_id: str,
    payload: TestCaseUpdate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(
            role_required(
                [UserRole.ADMIN]
            )
        ),
    ],
):
    return await TestCaseService.update_test_case(
        db,
        test_case_id,
        payload,
    )


@router.delete(
    "/test-cases/{test_case_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_test_case(
    test_case_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(
            role_required(
                [UserRole.ADMIN]
            )
        ),
    ],
):
    return await TestCaseService.delete_test_case(
        db,
        test_case_id,
    )