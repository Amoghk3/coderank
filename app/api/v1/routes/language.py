from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from app.models.enums import UserRole
from app.api.deps import require_roles
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user

from app.core.database import get_db

from app.models.user import User

from app.schemas.language_schema import (
    LanguageCreate,
    LanguageUpdate,
    LanguageResponse,
)

from app.services.language_service import (
    LanguageService,
)


router = APIRouter(
    prefix="/languages",
    tags=["Languages"],
)


@router.post(
    "",
    response_model=LanguageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_language(
    payload: LanguageCreate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
    User,
    Depends(
        require_roles(
            [UserRole.ADMIN]
        )
    ),
],
):
    return await LanguageService.create_language(
        db,
        payload,
    )


@router.get(
    "",
    response_model=list[LanguageResponse],
)
async def get_languages(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await LanguageService.get_languages(
        db,
    )


@router.get(
    "/{language_id}",
    response_model=LanguageResponse,
)
async def get_language(
    language_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await LanguageService.get_language(
        db,
        language_id,
    )


@router.put(
    "/{language_id}",
    response_model=LanguageResponse,
)
async def update_language(
    language_id: str,
    payload: LanguageUpdate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
    User,
        Depends(
            require_roles(
                [UserRole.ADMIN]
            )
        ),
    ],
):
    return await LanguageService.update_language(
        db,
        language_id,
        payload,
    )


@router.delete(
    "/{language_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_language(
    language_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    current_user: Annotated[
    User,
    Depends(
        require_roles(
            [UserRole.ADMIN]
        )
    ),
],
):
    return await LanguageService.delete_language(
        db,
        language_id,
    )