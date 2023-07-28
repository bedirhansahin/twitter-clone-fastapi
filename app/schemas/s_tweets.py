from pydantic import BaseModel


from datetime import datetime


class TweetBase(BaseModel):
    content: str


class TweetCreate(TweetBase):
    pass


class TweetUpdate(BaseModel):
    new_content: str


class Tweet(TweetBase):
    id: int
    user_id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class TweetResponse(BaseModel):
    tweetId: int
    userId: int
    username: str
    content: str
    created_at: datetime
