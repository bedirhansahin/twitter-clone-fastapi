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
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID

from database import Base
import uuid


class User(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4(), unique=True)
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
    follows = relationship(
        "Follows",
        back_populates="follows_user",
        foreign_keys="Follows.following_user_id",
    )
    followers = relationship("Follows", back_populates="user", foreign_keys="Follows.user_id")
    tweet_likes = relationship("TweetLikes", back_populates="user")
    comment_likes = relationship("CommentLikes", back_populates="user")

    def __repr__(self):
        return f"{self.id} | {self.username}"


class Tweet(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "tweets"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4(), unique=True)
    content = Column(String(255), index=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.users.id"))

    user = relationship("User", back_populates="tweets", foreign_keys=[user_id])
    comments = relationship("Comments", back_populates="tweet", cascade="all, delete-orphan")
    likes = relationship("TweetLikes", back_populates="tweet")


class Comments(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4(), unique=True)
    tweet_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.tweets.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.users.id"))
    content = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.comments.id"))

    tweet = relationship("Tweet", back_populates="comments", foreign_keys=[tweet_id])
    user = relationship("User", back_populates="comments", foreign_keys=[user_id])
    parent_comment = relationship(
        "Comments",
        remote_side=[id],
        backref=backref("child_posts", remote_side=[parent_comment_id]),
    )
    likes = relationship("CommentLikes", back_populates="comment")


class Follows(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "follows"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4(), unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.users.id"))
    following_user_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.users.id"))

    user = relationship("User", back_populates="follows", foreign_keys=[user_id])
    follows_user = relationship(
        "User", back_populates="followers", foreign_keys=[following_user_id]
    )


class TweetLikes(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "tweet_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.users.id"))
    tweet_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.tweets.id"))

    user = relationship("User", back_populates="tweet_likes", foreign_keys=[user_id])
    tweet = relationship("Tweet", back_populates="likes", foreign_keys=[tweet_id])


class CommentLikes(Base):
    __table_args__ = {"schema": "twitter_clone"}
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.users.id"))
    comment_id = Column(UUID(as_uuid=True), ForeignKey("twitter_clone.comments.id"))

    user = relationship("User", back_populates="comment_likes", foreign_keys=[user_id])
    comment = relationship("Comments", back_populates="likes", foreign_keys=[comment_id])
