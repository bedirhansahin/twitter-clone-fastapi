from fastapi import HTTPException
from sqlalchemy.orm import Session

from uuid import UUID

from cruds import c_users

import models


def create_comment_like_for_comment(db: Session, comment_id: UUID, user_id: UUID):
    already_comment_like = (
        db.query(models.CommentLikes)
        .filter(
            models.CommentLikes.user_id == user_id, models.CommentLikes.comment_id == comment_id
        )
        .one_or_none()
    )

    if already_comment_like:
        raise HTTPException(status_code=400, detail="Already liked the comment")

    comment_like = models.CommentLikes(user_id=user_id, comment_id=comment_id)
    db.add(comment_like)
    db.commit()
    db.refresh(comment_like)
    return comment_like


def get_all_comment_likes(db: Session):
    query = db.query(models.CommentLikes).all()
    return query


def get_likes_for_comment(db: Session, comment_id: UUID):
    query = db.query(models.CommentLikes).filter(models.CommentLikes.comment_id == comment_id).all()
    return query


def get_likes_for_user(db: Session, user_id: UUID):
    query = db.query(models.CommentLikes).filter(models.CommentLikes.user_id == user_id).all()
    return query


def delete_comment_like(db: Session, id: int, user_id: UUID):
    comment_like = db.query(models.CommentLikes).filter(models.CommentLikes.id == id).one_or_none()
    if not comment_like:
        raise HTTPException(status_code=400, detail="You already did not like this comment")

    user = c_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400)

    if user.id != comment_like.user_id:
        raise HTTPException(status_code=401, detail="You can not delete this comment")

    db.delete(comment_like)
    db.commit()
