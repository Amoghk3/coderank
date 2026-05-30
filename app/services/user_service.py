from fastapi import HTTPException

from app.models.user import User


class UserService:

    @staticmethod
    async def update_role(
        db,
        user_id: str,
        role,
    ):

        user = await db.get(
            User,
            user_id,
        )

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        user.role = role

        await db.commit()
        await db.refresh(user)

        return user