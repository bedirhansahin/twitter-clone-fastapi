from pydantic import BaseModel, EmailStr
from typing import Optional, List

from datetime import datetime, date


class UserBase(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str]
    birthdate: Optional[date]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_private: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    bio: Optional[str]
    birthdate: Optional[date]
