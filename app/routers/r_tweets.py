from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from typing import List, Optional

from schemas import s_tweets, s_users

from dependencies import get_db, get_current_user
from cruds import c_tweets, c_users

router = APIRouter()


@router.post("", response_model=s_tweets.TweetResponse)
def create_tweet(
    tweet_body: s_tweets.TweetCreate,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    tweet = c_tweets.create_tweet(db=db, tweet=tweet_body, user_id=current_user.id)
    return s_tweets.TweetResponse(
        tweetId=tweet.id,
        userId=tweet.user.id,
        content=tweet.content,
        created_at=tweet.created_at,
        username=tweet.user.username,
    )


@router.get("/", response_model=List[s_tweets.TweetResponse])
def get_all_tweets(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    if user_id:
        user = c_users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist.")
        tweets = c_tweets.get_users_tweets(db, user_id, skip, limit)
    else:
        tweets = c_tweets.get_all_tweets(db, skip, limit)

    return [
        s_tweets.TweetResponse(
            tweetId=tweet.id,
            content=tweet.content,
            created_at=tweet.created_at,
            userId=tweet.user.id,
            username=tweet.user.username,
        )
        for tweet in tweets
    ]


@router.get("/tweet/{tweet_id}", response_model=s_tweets.TweetResponse)
def get_tweet_by_tweet_id(tweet_id: int, db: Session = Depends(get_db)):
    tweet = c_tweets.get_tweet_by_id(db, tweet_id)

    return s_tweets.TweetResponse(
        tweetId=tweet.id,
        content=tweet.content,
        userId=tweet.user.id,
        username=tweet.user.username,
        created_at=tweet.created_at,
    )
