from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from typing import List

from dependencies import get_db
from schemas import s_users
from cruds import c_users


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[s_users.UserResponse])
def get_all_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = c_users.get_all_users(db, skip, limit)
    return users
