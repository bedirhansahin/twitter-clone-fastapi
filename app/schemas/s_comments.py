from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class CommentBase(BaseModel):
    id: int
    user_id: int
    tweet_id: int
    content: str
    created_at: datetime


class Comment(CommentBase):
    username: str

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str
    tweet_id: Optional[int]


class CommentDelete(BaseModel):
    comment_id: int


class CommentUpdate(BaseModel):
    comment_id: int
    new_content: str
