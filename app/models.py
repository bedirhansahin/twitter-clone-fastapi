from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    bio = Column(String)
    birthdate = Column(Date)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tweets = relationship("Tweet", back_populates="user")
    comments = relationship("Comments", back_populates="user")

    def __repr__(self):
        return f"{self.id} | {self.username}"


class Tweet(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), index=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("twitter_clone.users.id"))

    user = relationship("User", back_populates="tweets", foreign_keys=[user_id])
    comments = relationship(
        "Comments", back_populates="tweet", cascade="all, delete-orphan"
    )


class Comments(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("twitter_clone.tweets.id"))
    user_id = Column(Integer, ForeignKey("twitter_clone.users.id"))
    content = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())

    tweet = relationship("Tweet", back_populates="comments", foreign_keys=[tweet_id])
    user = relationship("User", back_populates="comments", foreign_keys=[user_id])
