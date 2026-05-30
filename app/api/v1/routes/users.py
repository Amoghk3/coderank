from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
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

from app.schemas.user_schema import (
    UpdateUserRoleRequest,
)

from app.services.user_service import (
    UserService,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.patch("/{user_id}/role")
async def update_user_role(
    user_id: str,
    payload: UpdateUserRoleRequest,

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

    return await UserService.update_role(
        db,
        user_id,
        payload.role,
    )