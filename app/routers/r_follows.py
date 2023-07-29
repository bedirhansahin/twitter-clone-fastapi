from fastapi import APIRouter, Depends, HTTPException

from typing import List

from sqlalchemy.orm import Session

from schemas import s_users, s_followers, s_counts
from cruds import c_follows, c_counts, c_users
from dependencies import get_current_user, get_db

router = APIRouter()


@router.post("")
async def create_follow_for_user(
    request_body: s_followers.FollowCreateOrDeleteRequestBody,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    c_follows.create_follow(db, current_user.id, request_body.follow_user_id)
    return {"message": "Success"}


@router.get("/count/follows/{user_id}", response_model=s_counts.CountBase)
def get_follows_count_for_user(user_id: int, db: Session = Depends(get_db)):
    count = c_counts.get_following_for_user(db, user_id)
    return s_counts.CountBase(count=count)


@router.get("/count/followers/{user_id}", response_model=s_counts.CountBase)
def get_followers_count_for_user(user_id: int, db: Session = Depends(get_db)):
    count = c_counts.get_followers_for_user(db, user_id)
    return s_counts.CountBase(count=count)


@router.get("/follows/{user_id}", response_model=List[s_followers.FollowResponseBody])
def get_all_follows_for_user(user_id: int, db: Session = Depends(get_db)):
    user = c_users.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User does not found")

    follows = c_follows.get_all_user_follows(db, user_id)
    return [
        s_followers.FollowResponseBody(
            user_id=follow.follows_user.id,
            email=follow.follows_user.email,
            username=follow.follows_user.username,
            bio=follow.follows_user.bio,
            birthdate=follow.follows_user.birthdate,
        )
        for follow in follows
    ]


@router.get(
    "/followers/{user_id}", response_model=List[s_followers.FollowerResponseBody]
)
def get_all_followers_for_user(user_id: int, db: Session = Depends(get_db)):
    user = c_users.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User does not found")

    followers = c_follows.get_all_user_followers(db, user_id)

    return [
        s_followers.FollowerResponseBody(
            user_id=follower.user.id,
            email=follower.user.email,
            username=follower.user.username,
            bio=follower.user.bio,
            birthdate=follower.user.birthdate,
        )
        for follower in followers
    ]


@router.delete("")
async def delete_follow_for_user(
    request_body: s_followers.FollowCreateOrDeleteRequestBody,
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    c_follows.delete_follow(db, current_user.id, request_body.follow_user_id)
    return {"messages": "Delete Successfully"}
