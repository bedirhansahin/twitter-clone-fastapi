from sqlalchemy.orm import Session

from typing import Union, Optional
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from schemas import s_users
from cruds import c_users


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(token: str):
    """Return a dictionary that represents the decoded JWT."""
    return jwt.decode(token, "secret_key", algorithms=["HS256"])


def authenticate_user(
    db: Session, email: str, password: str
) -> Union[bool, s_users.User]:
    user = c_users.get_user_by_email_or_username(db, username=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm="HS256")
    return encoded_jwt
