from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import Optional

import models
from schemas import s_comments, s_tweets

from uuid import UUID, uuid4


def create_comment(
    db: Session,
    user_id: UUID,
    comment: s_comments.CommentCreate,
    parent_comment_id: Optional[UUID] = None,
):
    db_tweet: s_tweets.Tweet = (
        db.query(models.Tweet).filter(models.Tweet.id == comment.tweet_id).one_or_none()
    )
    if not db_tweet:
        raise HTTPException(status_code=400, detail="Tweet does not exist")

    new_id = uuid4()

    db_parent_comment = (
        db.query(models.Comments).filter(models.Comments.id == parent_comment_id).one_or_none()
    )
    if parent_comment_id:
        if not db_parent_comment:
            raise HTTPException(status_code=400, detail="Parent comment does not exist")

    db_comment = models.Comments(
        tweet_id=comment.tweet_id,
        user_id=user_id,
        content=comment.content,
        parent_comment_id=comment.parent_comment_id,
    )

    db_comment.id = new_id
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    except Exception:
        raise HTTPException(status_code=400, detail="Tweet does not exist")


def get_comment_by_id(db: Session, comment_id: UUID) -> models.Comments:
    query = db.query(models.Comments).filter(models.Comments.id == comment_id).one_or_none()
    return query


def get_comments_for_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 0):
    db_user = db.query(models.User).filter(models.User.id == user_id).one_or_none()

    return (
        db.query(models.Comments)
        .filter(models.Comments.user_id == user_id)
        .order_by(models.Comments.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_comments_for_tweet(db: Session, tweet_id: UUID, skip: int = 0, limit: int = 0):
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()

    if not db_tweet:
        raise HTTPException(status_code=400, detail="Tweet does not exist")

    return (
        db.query(models.Comments)
        .filter(models.Comments.tweet_id == tweet_id)
        .order_by(models.Comments.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_comment(
    db: Session, comment: s_comments.CommentUpdate, user_id: UUID
) -> s_comments.Comment:
    db_comment: s_comments.Comment = (
        db.query(models.Comments).filter(models.Comments.id == comment.comment_id).one_or_none()
    )
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment does not exist")

    if db_comment.user_id != user_id:
        raise HTTPException(status_code=401, detail="User does not own this comment")

    db_comment.content = comment.new_content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment: s_comments.CommentDelete, user_id: UUID):
    db_comment: s_comments.Comment = (
        db.query(models.Comments).filter(models.Comments.id == comment.comment_id).one_or_none()
    )
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment does not exist")

    if db_comment.user_id != user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to delete that comment")

    try:
        db.delete(db_comment)
        db.commit()

    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")
