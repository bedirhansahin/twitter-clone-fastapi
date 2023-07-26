from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status

from sqlalchemy.orm import Session

from typing import List

from dependencies import get_db, send_email_notification, get_current_user
from schemas import s_users
from cruds import c_users
import security


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=s_users.User)
async def create_user(
    user: s_users.UserCreate, bg_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    db_user = c_users.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    newUser: s_users.User = c_users.create_user(db=db, user=user)
    bg_tasks.add_task(
        send_email_notification, username=newUser.username, email=newUser.email
    )
    return newUser


@router.get("", response_model=List[s_users.UserResponse])
def get_all_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = c_users.get_all_users(db, skip, limit)
    return users


@router.get("/me", response_model=s_users.User)
def get_authenticated_user(
    db: Session = Depends(get_db),
    current_user: s_users.User = Depends(get_current_user),
):
    return current_user
