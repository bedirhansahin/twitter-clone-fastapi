from pydantic import BaseModel


from datetime import datetime

from uuid import UUID


class TweetBase(BaseModel):
    content: str


class TweetCreate(TweetBase):
    pass


class TweetUpdate(BaseModel):
    new_content: str


class Tweet(TweetBase):
    id: UUID
    user_id: UUID
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class TweetResponse(BaseModel):
    tweetId: UUID
    userId: UUID
    username: str
    content: str
    created_at: datetime
