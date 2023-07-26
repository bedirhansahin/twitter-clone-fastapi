from pydantic import BaseModel, EmailStr
from typing import Optional

from datetime import datetime, date


class TweetBase(str):
    content: str


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    userId: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
