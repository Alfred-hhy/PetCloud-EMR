from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

UserRole = Literal["OWNER", "VET", "CLINIC_ADMIN"]


class UserBase(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, description="密码至少 6 位")
    full_name: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
