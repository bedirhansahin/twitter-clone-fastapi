from pydantic import BaseModel
from typing import Optional

from datetime import datetime
from uuid import UUID


class CommentBase(BaseModel):
    id: UUID
    user_id: UUID
    tweet_id: UUID
    content: str
    created_at: datetime


class Comment(CommentBase):
    username: str

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str
    tweet_id: Optional[UUID]


class CommentDelete(BaseModel):
    comment_id: UUID


class CommentUpdate(BaseModel):
    comment_id: UUID
    new_content: str
