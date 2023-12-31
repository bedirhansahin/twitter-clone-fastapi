from fastapi import HTTPException
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from schemas import s_users
import security
import models

from uuid import UUID, uuid4


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    query = (
        db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()
    )
    return query


def get_user_by_email(db: Session, email: str):
    query = db.query(models.User).filter(models.User.email == email).one_or_none()
    return query


def get_user_by_username(db: Session, username: str):
    query = (
        db.query(models.User)
        .filter(
            models.User.username == username,
        )
        .filter(
            models.User.is_active == True,
        )
        .one_or_none()
    )
    return query


def get_user_by_id(db: Session, user_id: UUID):
    query = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    return query


def search_user_by_username_letters(db: Session, username: str, skip: int = 0, limit: int = 10):
    query = (
        db.query(models.User)
        .filter(
            or_(
                models.User.username.ilike(f"%{username}%"),
            )
        )
        .filter(
            models.User.is_active == True,
        )
        .limit(limit)
        .offset(skip)
        .all()
    )
    return query


def get_user_by_email_or_username(db: Session, username: str):
    query = (
        db.query(models.User)
        .filter(
            or_(
                func.lower(models.User.email) == func.lower(username),
                func.lower(models.User.username) == func.lower(username),
            )
        )
        .first()
    )
    return query


def create_user(db: Session, user: s_users.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    new_id = uuid4()
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        bio=user.bio,
        birthdate=user.birthdate,
    )
    db_user.id = new_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: UUID, user_update: s_users.UserUpdateRequest):
    user_db = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if user_update.newBio:
        user_db.bio = user_update.newBio

    if user_update.newUsername:
        user_db.username = user_update.newUsername

    if user_update.newBirthdate:
        user_db.birthdate = user_update.newBirthdate

    db.commit()
    db.refresh(user_db)
    return user_db


def change_password(db: Session, user_id: UUID, password_update: s_users.UserChangePasswordRequest):
    user_db = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if password_update.newPassword == password_update.newPassword2:
        user_db.hashed_password = security.get_password_hash(password_update.newPassword)
    else:
        raise HTTPException(status_code=400, detail="Passwords do not match!")

    db.commit()
    db.refresh(user_db)
    return user_db


def delete_user(db: Session, user_id: UUID):
    try:
        db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def change_user_private_status(db: Session, user_id: UUID):
    user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if user:
        user.is_private = not user.is_private
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")


def change_user_active_status(db: Session, user_id: UUID):
    user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if user:
        user.is_active = not user.is_active
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")
