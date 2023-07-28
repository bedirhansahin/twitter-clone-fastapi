from fastapi import HTTPException

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from typing import List, Union, Optional

import models
from schemas import s_tweets


def get_all_tweets(db: Session, skip: int = 0, limit: int = 10):
    query = (
        db.query(models.Tweet)
        .order_by(models.Tweet.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return query


def get_tweet_by_id(db: Session, tweet_id: int):
    query = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()
    return query


def get_users_tweets(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    db_user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")

    query = (
        db.query(models.Tweet)
        .filter(models.Tweet.user_id == user_id)
        .order_by(models.Tweet.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return query


def create_tweet(db: Session, tweet: s_tweets.TweetCreate, user_id: int):
    db_tweet = models.Tweet(**tweet.dict())
    db_tweet.user_id = user_id

    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def update_tweet(db: Session, tweet_id: int, user_id: int, new_content: str):
    db_tweet: s_tweets.Tweet = (
        db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()
    )

    if not db_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    if db_tweet.user_id != user_id:
        raise HTTPException(status_code=401, detail="User does not own this tweet")

    db_tweet.content = new_content
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def delete_tweet(db: Session, tweet_id: int, user_id: int):
    db_tweet: s_tweets.Tweet = (
        db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()
    )

    if not db_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    if db_tweet.user_id != user_id:
        raise HTTPException(status_code=401, detail="User does not own this tweet")

    try:
        db.delete(db_tweet)
        db.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")
