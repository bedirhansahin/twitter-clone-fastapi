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


class UserUpdateBody(BaseModel):
    id: int
    email: EmailStr
    username: str
    bio: Optional[str]
    birthdate: Optional[date]

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    password: str
    newUsername: Optional[str] = None
    newBio: Optional[str] = None


class UserChangePasswordRequest(BaseModel):
    password: str
    newPassword: str
    newPassword2: str


class UserPasswordBody(User):
    hashed_password: str

    class Config:
        from_attributes = True


class UserDeleteRequest(BaseModel):
    password: str
