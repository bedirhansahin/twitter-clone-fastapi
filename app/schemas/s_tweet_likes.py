from pydantic import BaseModel

from typing import Optional

from uuid import UUID


class BasicTweet(BaseModel):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class BasicUser(BaseModel):
    id: UUID
    email: str
    username: str

    class Config:
        from_attributes = True


class TweetLike(BaseModel):
    tweet_id: UUID
    tweet: BasicTweet
    user: BasicUser

    class Config:
        from_attributes = True


class TweetLikeCreateOrDeleteRequest(BaseModel):
    tweet_id: UUID


class TweetLikeResponseBody(BaseModel):
    tweet_id: UUID
    user_id: UUID
    username: str
