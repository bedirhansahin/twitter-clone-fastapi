from sqlalchemy.orm import Session

import models


def get_comment_count_for_tweet(db: Session, tweet_id: int):
    count = (
        db.query(models.Comments).filter(models.Comments.tweet_id == tweet_id).count()
    )
    return count
