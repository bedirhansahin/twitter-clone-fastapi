from fastapi import HTTPException

from sqlalchemy.orm import Session

import models


def get_all_user_follows(db: Session, user_id: int):
    query = db.query(models.Follows).filter(models.Follows.user_id == user_id).all()

    return query


def get_all_user_followers(db: Session, user_id: int):
    user = db.query(models.User.id).filter(models.User.id == user_id).one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    followers = (
        db.query(models.Follows)
        .filter(models.Follows.following_user_id == user_id)
        .all()
    )
    return followers


def create_follow(db: Session, user_id: int, follow_user_id: int):
    user = db.query(models.User).filter(models.User.id == follow_user_id).one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    already_follow = (
        db.query(models.Follows)
        .filter(
            models.Follows.user_id == user_id,
            models.Follows.following_user_id == follow_user_id,
        )
        .one_or_none()
    )
    if already_follow:
        raise HTTPException(status_code=400, detail="Already Following User")

    db_follows = models.Follows(user_id=user_id, following_user_id=follow_user_id)
    db.add(db_follows)
    db.commit()
    db.refresh(db_follows)
    return db_follows


def delete_follow(db: Session, user_id: int, follow_user_id: int):
    user = db.query(models.User).filter(models.User.id == follow_user_id).one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    already_follow = (
        db.query(models.Follows)
        .filter(
            models.Follows.user_id == user_id,
            models.Follows.following_user_id == follow_user_id,
        )
        .one_or_none()
    )

    if not already_follow:
        raise HTTPException(
            status_code=400,
            detail="Cannot unfollow the user that is not being followed",
        )

    db.delete(already_follow)
    db.commit()
    return {}
