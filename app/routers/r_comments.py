from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from typing import List

from schemas import s_comments, s_users, s_counts
from cruds import c_comments, c_counts
from dependencies import get_db, get_current_user, is_valid_uuid

from uuid import UUID


router = APIRouter()


@router.post("", response_model=s_comments.Comment)
async def create_comment(
    request_body: s_comments.CommentCreate,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    new_comment = c_comments.create_comment(db, current_user.id, request_body)
    return s_comments.Comment(
        id=new_comment.id,
        user_id=new_comment.user.id,
        tweet_id=new_comment.tweet.id,
        username=new_comment.user.username,
        content=new_comment.content,
        created_at=new_comment.created_at,
        parent_comment_id=new_comment.parent_comment_id,
    )


@router.get("/user/{user_id}", response_model=List[s_comments.Comment])
def get_comments_for_user(
    user_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    if not is_valid_uuid(user_id):
        raise HTTPException(status_code=400, detail="User does not exist")
    comments = c_comments.get_comments_for_user(db, user_id, skip, limit)
    return [
        s_comments.Comment(
            id=comment.id,
            user_id=comment.user_id,
            username=comment.user.username,
            tweet_id=comment.tweet_id,
            content=comment.content,
            created_at=comment.created_at,
        )
        for comment in comments
    ]


@router.get("/tweet/{tweet_id}", response_model=List[s_comments.Comment])
def get_comments_for_tweet(
    tweet_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    comments = c_comments.get_comments_for_tweet(db, tweet_id, skip, limit)
    return [
        s_comments.Comment(
            id=comment.id,
            user_id=comment.user_id,
            username=comment.user.username,
            tweet_id=comment.tweet_id,
            content=comment.content,
            created_at=comment.created_at,
        )
        for comment in comments
    ]


@router.get("/comment/{comment_id}", response_model=s_comments.Comment)
def get_comment_by_id(comment_id: UUID, db: Session = Depends(get_db)):
    comment = c_comments.get_comment_by_id(db, comment_id)
    return s_comments.Comment(
        id=comment.id,
        user_id=comment.user_id,
        username=comment.user.username,
        tweet_id=comment.tweet_id,
        content=comment.content,
        created_at=comment.created_at,
    )


@router.get("/count/tweet/{tweet_id}", response_model=s_counts.CountBase)
def get_comment_count_for_tweet(tweet_id: UUID, db: Session = Depends(get_db)):
    count = c_counts.get_comment_count_for_tweet(db, tweet_id)
    return s_counts.CountBase(count=count)


@router.put("", response_model=s_comments.Comment)
async def update_comment(
    request_body: s_comments.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    comment = c_comments.update_comment(db, request_body, current_user.id)
    return s_comments.Comment(
        id=comment.id,
        user_id=comment.user_id,
        tweet_id=comment.tweet_id,
        content=comment.content,
        created_at=comment.created_at,
        username=comment.user.username,
    )


@router.delete(
    "",
)
async def delete_comment(
    request_body: s_comments.CommentDelete,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    c_comments.delete_comment(db, request_body, current_user.id)
    return {"message": "Comment deleted successfully"}
