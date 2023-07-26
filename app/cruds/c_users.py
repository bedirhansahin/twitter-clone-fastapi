from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from schemas import s_users
import security
import models


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(models.User).offset(skip).limit(limit).all()
    return query


def get_user_by_email(db: Session, email: str):
    query = db.query(models.User).filter(models.User.email == email).one_or_none()
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
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
