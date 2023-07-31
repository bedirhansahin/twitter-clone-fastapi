from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from typing import List

from schemas import s_tweet_likes, s_users, s_counts
from cruds import c_tweet_likes, c_counts
from dependencies import get_db, get_current_user

from uuid import UUID


router = APIRouter()


@router.post("")
async def like_tweet(
    request_body: s_tweet_likes.TweetLikeCreateOrDeleteRequest,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    c_tweet_likes.create_tweet_like_for_tweet(db, request_body.tweet_id, current_user.id)

    return {"messages": "Tweet liked successfully"}


@router.get("/count/tweet/{tweet_id}", response_model=s_counts.CountBase)
def get_likes_count_for_tweet(tweet_id: UUID, db: Session = Depends(get_db)):
    count = c_counts.get_count_like_for_tweet(db, tweet_id)
    return s_counts.CountBase(count=count)


@router.get("/count/user/{user_id}", response_model=s_counts.CountBase)
def get_likes_count_for_user(user_id: UUID, db: Session = Depends(get_db)):
    count = c_counts.get_count_like_for_user(db, user_id)
    return s_counts.CountBase(count=count)


@router.get("/likes/{user_id}", response_model=List[s_tweet_likes.TweetLikeResponseBody])
def get_likes_for_user(user_id: UUID, db: Session = Depends(get_db)):
    tweets = c_tweet_likes.get_likes_for_user(db, user_id)
    return [
        s_tweet_likes.TweetLikeResponseBody(
            tweet_id=tweet.tweet_id, user_id=tweet.user_id, username=tweet.user.username
        )
        for tweet in tweets
    ]


@router.delete("")
def delete_tweet_like(
    id: int,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    c_tweet_likes.delete_tweet_like(db, id=id, user_id=current_user.id)
    return {"messages": "Tweet like deleted successfully"}
