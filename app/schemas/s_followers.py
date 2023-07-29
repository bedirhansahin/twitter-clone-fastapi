from pydantic import BaseModel

from typing import Optional

from datetime import date


class BasicUser(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Follower(BaseModel):
    user: BasicUser
    follow_user: BasicUser

    class Config:
        from_attributes = True


class FollowerRequestBody(BaseModel):
    user_id: int


class FollowerResponseBody(BaseModel):
    user_id: int
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]


class Follow(BaseModel):
    user: BasicUser
    follow_user: BasicUser


class FollowCreateOrDeleteRequestBody(BaseModel):
    follow_user_id: int


class FollowResponseBody(BaseModel):
    user_id: int
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]

    class Config:
        from_attributes = True
