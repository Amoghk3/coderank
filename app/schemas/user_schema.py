from pydantic import BaseModel, EmailStr

from app.models.enums import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class UpdateUserRoleRequest(
    BaseModel
):
    role: UserRole