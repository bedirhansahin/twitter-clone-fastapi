from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Response

from sqlalchemy.orm import Session

from typing import List

from dependencies import get_db, send_email_notification, get_current_user, is_valid_uuid
from schemas import s_users
from cruds import c_users
import security


router = APIRouter()


@router.post("", response_model=s_users.User)
async def create_user(
    user: s_users.UserCreate, bg_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    db_user_email = c_users.get_user_by_email(db, user.email)
    db_user_username = c_users.get_user_by_username(db, user.username)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    newUser: s_users.User = c_users.create_user(db=db, user=user)
    bg_tasks.add_task(send_email_notification, username=newUser.username, email=newUser.email)
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


@router.get("/search/{username}", response_model=List[s_users.UserResponse])
def get_one_or_all_users(
    username: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    users = c_users.search_user_by_username_letters(
        db=db, username=username, skip=skip, limit=limit
    )
    return users


@router.get("/{username}", response_model=s_users.UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = c_users.get_user_by_username(db, username)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/me", response_model=s_users.UserUpdateBody)
async def update_user(
    request_body: s_users.UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: s_users.UserPasswordBody = Depends(get_current_user),
):
    if not security.verify_password(request_body.password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    if request_body.newUsername is not None:
        db_user_with_username = c_users.get_user_by_username(db, request_body.newUsername)

        if db_user_with_username is not None:
            raise HTTPException(status_code=406, detail="Username already exists")

    if not is_valid_uuid(current_user.id):
        raise HTTPException(status_code=400, detail="Tweet does not exist")

    user = c_users.update_user(db, current_user.id, request_body)
    return user


@router.put("/changePassword")
async def change_password(
    request_body: s_users.UserChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: s_users.UserPasswordBody = Depends(get_current_user),
):
    if not security.verify_password(request_body.password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    c_users.change_password(db, current_user.id, request_body)
    response = Response(content="Password changed successfully")
    response.status_code = 200
    return response


@router.delete(
    "/me",
)
async def delete_user(
    request_body: s_users.UserDeleteRequest,
    db: Session = Depends(get_db),
    current_user: s_users.UserPasswordBody = Depends(get_current_user),
):
    if not security.verify_password(request_body.password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    c_users.delete_user(db, current_user.id)
    return {"message": "User deleted successfuly"}


@router.put("/settings/safety")
def change_private_or_public(
    db: Session = Depends(get_db),
    current_user: s_users.UserPasswordBody = Depends(get_current_user),
):
    updated_user = c_users.change_user_private_status(db, current_user.id)

    if updated_user:
        return {"message": "User status is changed"}
    else:
        return {"error": "User not found"}


@router.put("/settings/status")
def change_active_status(
    db: Session = Depends(get_db),
    current_user: s_users.UserPasswordBody = Depends(get_current_user),
):
    updated_user = c_users.change_user_active_status(db, current_user.id)

    if updated_user:
        return {"message": "User status is changed"}
    else:
        return {"error": "User not found"}
