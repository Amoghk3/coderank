from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
)


class AuthService:

    @staticmethod
    async def register(
        db: AsyncSession,
        payload: UserCreate,
    ):
        logger.info(
            f"Register request received for email={payload.email}"
        )

        existing_user = await UserRepository.get_by_email(
            db,
            payload.email,
        )

        if existing_user:
            logger.warning(
                f"Registration failed. Email already exists: {payload.email}"
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            email=payload.email,
            username=payload.username,
            password_hash=hash_password(
                payload.password
            ),
        )

        created_user = await UserRepository.create_user(
            db,
            user,
        )

        logger.success(
            f"User registered successfully: {created_user.email}"
        )

        return {
            "message": "User registered successfully",
            "user": {
                "id": str(created_user.id),
                "email": created_user.email,
                "username": created_user.username,
                "is_active": created_user.is_active,
            },
        }

    @staticmethod
    async def login(
        db: AsyncSession,
        payload: UserLogin,
    ):
        logger.info(
            f"Login request received for email={payload.email}"
        )

        user = await UserRepository.get_by_email(
            db,
            payload.email,
        )

        if not user:
            logger.warning(
                f"Login failed. User not found: {payload.email}"
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not verify_password(
            payload.password,
            user.password_hash,
        ):
            logger.warning(
                f"Login failed. Invalid password for: {payload.email}"
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        logger.success(
            f"User logged in successfully: {user.email}"
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
            },
        }

    @staticmethod
    async def get_current_user(
        current_user: User,
    ):
        logger.info(
            f"Fetched profile for user={current_user.email}"
        )

        return {
            "id": str(current_user.id),
            "email": current_user.email,
            "username": current_user.username,
            "is_active": current_user.is_active,
        }

    @staticmethod
    async def logout(
        current_user: User,
    ):
        logger.info(
            f"User logged out: {current_user.email}"
        )

        return {
            "message": "Logged out successfully"
        }