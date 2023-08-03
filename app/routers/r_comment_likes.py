from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from typing import List

from dependencies import get_db, get_current_user
from cruds import c_comment_likes, c_counts
from schemas import s_users, s_comment_likes, s_counts

from uuid import UUID


router = APIRouter()


@router.post("")
async def like_comment(
    request_body: s_comment_likes.CommentLikeCreateOrDelete,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    c_comment_likes.create_comment_like_for_comment(db, request_body.comment_id, current_user.id)
    return {"messages": "Comment liked successfully"}


@router.get("/count/comment/{comment_id}", response_model=s_counts.CountBase)
def get_count_coment_like_for_comment(comment_id: UUID, db: Session = Depends(get_db)):
    count = c_counts.get_count_comment_like_for_comment(db, comment_id)
    return s_counts.CountBase(count=count)


@router.get("/count/user/{user_id}", response_model=s_counts.CountBase)
def get_count_coment_like_for_user(user_id: UUID, db: Session = Depends(get_db)):
    count = c_counts.get_count_comment_like_for_user(db, user_id)
    return s_counts.CountBase(count=count)


@router.get("/likes/{user_id}", response_model=List[s_comment_likes.CommentLikeResponseBody])
def get_likes_for_user(user_id: UUID, db: Session = Depends(get_db)):
    comments = c_comment_likes.get_likes_for_user(db, user_id)
    return [
        s_comment_likes.CommentLikeResponseBody(
            comment_id=comment.comment_id,
            user_id=comment.user_id,
            username=comment.user.username,
        )
        for comment in comments
    ]


@router.delete("")
def delete_comment_like(
    id: int, db: Session = Depends(get_db), current_user: s_users.User = Depends(get_current_user)
):
    c_comment_likes.delete_comment_like(db, id=id, user_id=current_user.id)
    return {"messages": "Comment deleted successfully"}
