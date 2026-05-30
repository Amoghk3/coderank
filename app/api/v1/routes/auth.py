from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(
    payload: UserCreate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    return await AuthService.register(
        db,
        payload,
    )


@router.post("/login")
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],

    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    return await AuthService.login(
        db,
        form_data,
    )


@router.get("/me")
async def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await AuthService.get_current_user(
        current_user
    )


@router.post("/logout")
async def logout(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return await AuthService.logout(
        current_user
    )