from fastapi import HTTPException
from sqlalchemy.orm import Session

from uuid import UUID

import models
from cruds import c_users


def create_tweet_like_for_tweet(db: Session, tweet_id: UUID, user_id: UUID):
    already_tweet_like = (
        db.query(models.TweetLikes)
        .filter(models.TweetLikes.user_id == user_id, models.TweetLikes.tweet_id == tweet_id)
        .one_or_none()
    )
    if already_tweet_like:
        raise HTTPException(status_code=400, detail="Already liked the tweet")

    tweet_like = models.TweetLikes(user_id=user_id, tweet_id=tweet_id)
    db.add(tweet_like)
    db.commit()
    db.refresh(tweet_like)
    return tweet_like


def get_all_tweet_likes(db: Session):
    query = db.query(models.TweetLikes).all()
    return query


def get_likes_for_tweet(db: Session, tweet_id: UUID):
    query = db.query(models.TweetLikes).filter(models.TweetLikes.tweet_id == tweet_id).all()
    return query


def get_likes_for_user(db: Session, user_id: UUID):
    query = db.query(models.TweetLikes).filter(models.TweetLikes.user_id == user_id).all()
    return query


def delete_tweet_like(db: Session, id: int, user_id: UUID):
    tweet_like = db.query(models.TweetLikes).filter(models.TweetLikes.id == id).one_or_none()
    if not tweet_like:
        raise HTTPException(status_code=400)

    user = c_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400)

    if user.id != tweet_like.user_id:
        raise HTTPException(status_code=401)

    db.delete(tweet_like)
    db.commit()
