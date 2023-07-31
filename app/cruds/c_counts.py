from sqlalchemy.orm import Session

import models

from uuid import UUID


def get_comment_count_for_tweet(db: Session, tweet_id: UUID):
    count = db.query(models.Comments).filter(models.Comments.tweet_id == tweet_id).count()
    return count


def get_following_for_user(db: Session, user_id: UUID):
    count = db.query(models.Follows).filter(models.Follows.user_id == user_id).count()
    return count


def get_followers_for_user(db: Session, user_id: UUID):
    count = db.query(models.Follows).filter(models.Follows.following_user_id == user_id).count()
    return count


def get_count_like_for_tweet(db: Session, tweet_id: UUID):
    count = db.query(models.TweetLikes).filter(models.TweetLikes.tweet_id == tweet_id).count()
    return count


def get_count_like_for_user(db: Session, user_id: UUID):
    count = db.query(models.TweetLikes).filter(models.TweetLikes.user_id == user_id).count()
    return count
