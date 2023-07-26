from sqlalchemy.orm import Session

from schemas import s_users
import models


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(models.User).offset(skip).limit(limit).all()
    return query


def create_user(db: Session, user: s_users.UserCreate):
    hashed_password = user.password + "hashed"
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
