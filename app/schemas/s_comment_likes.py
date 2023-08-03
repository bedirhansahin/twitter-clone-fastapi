from pydantic import BaseModel

from uuid import UUID


class BasicComment(BaseModel):
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


class CommentLike(BaseModel):
    comment_id: UUID
    comment: BasicComment
    user: BasicUser

    class Config:
        from_attributes = True


class CommentLikeCreateOrDelete(BaseModel):
    comment_id: UUID


class CommentLikeResponseBody(BaseModel):
    comment_id: UUID
    user_id: UUID
    username: str
