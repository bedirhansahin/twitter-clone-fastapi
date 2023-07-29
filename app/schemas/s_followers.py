from pydantic import BaseModel

from typing import Optional

from datetime import date
from uuid import UUID


class BasicUser(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class Follower(BaseModel):
    user: BasicUser
    follow_user: BasicUser

    class Config:
        from_attributes = True


class FollowerRequestBody(BaseModel):
    user_id: UUID


class FollowerResponseBody(BaseModel):
    user_id: UUID
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]


class Follow(BaseModel):
    user: BasicUser
    follow_user: BasicUser


class FollowCreateOrDeleteRequestBody(BaseModel):
    follow_user_id: UUID


class FollowResponseBody(BaseModel):
    user_id: UUID
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]

    class Config:
        from_attributes = True
