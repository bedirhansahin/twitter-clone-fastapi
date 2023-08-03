from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import or_

from typing import Optional

import models
from schemas import s_tweets

from uuid import UUID, uuid4


def get_all_tweets(db: Session, skip: int = 0, limit: int = 10):
    query = (
        db.query(models.Tweet)
        .order_by(models.Tweet.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return query


def get_tweet_by_id(db: Session, tweet_id: UUID):
    query = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()
    return query


def get_users_tweets(db: Session, user_id: UUID, skip: int = 0, limit: int = 10):
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


def create_tweet(db: Session, tweet: s_tweets.TweetCreate, user_id: UUID):
    new_id = uuid4()
    db_tweet = models.Tweet(content=tweet.content)
    db_tweet.user_id = user_id
    db_tweet.id = new_id

    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def update_tweet(db: Session, tweet_id: UUID, user_id: UUID, new_content: str):
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


def delete_tweet(db: Session, tweet_id: UUID, user_id: UUID):
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


def search_tweet(db: Session, tweet_word: str):
    if tweet_word.lower().startswith("from: "):
        username_and_tweet_content = tweet_word[len("from: ") :].strip().split(" ", 1)
        username = username_and_tweet_content[0]
        tweet_content = username_and_tweet_content[1] if len(username_and_tweet_content) > 1 else ""

        user = db.query(models.User).filter(models.User.username == username).one_or_none()
        if user:
            if tweet_content:
                tweet = (
                    db.query(models.Tweet)
                    .filter(
                        models.Tweet.user_id == user.id,
                        or_(models.Tweet.content.ilike(f"%{tweet_content}%")),
                    )
                    .all()
                )
            else:
                tweet = db.query(models.Tweet).filter(models.Tweet.user_id == user.id).all()
        else:
            raise HTTPException(status_code=400, detail="User does not found")
    else:
        tweet = (
            db.query(models.Tweet).filter(or_(models.Tweet.content.ilike(f"%{tweet_word}%"))).all()
        )
    return tweet
