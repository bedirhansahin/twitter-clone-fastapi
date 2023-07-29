from sqlalchemy.orm import Session

import models


def get_comment_count_for_tweet(db: Session, tweet_id: int):
    count = db.query(models.Comments).filter(models.Comments.tweet_id == tweet_id).count()
    return count


def get_following_for_user(db: Session, user_id: int):
    count = db.query(models.Follows).filter(models.Follows.user_id == user_id).count()
    return count


def get_followers_for_user(db: Session, user_id: int):
    count = db.query(models.Follows).filter(models.Follows.following_user_id == user_id).count()
    return count
