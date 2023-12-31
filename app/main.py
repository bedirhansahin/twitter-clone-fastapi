from fastapi import FastAPI

from routers import r_users, r_auth, r_tweets, r_comments, r_follows, r_tweet_likes, r_comment_likes
from database import engine, Base

from dotenv import load_dotenv
import os

load_dotenv()


Base.metadata.create_all(bind=engine)


def main():
    return mount_versions()


TITLE = "Twitter Clone API"
CONTACT = "bedirhannsahin@gmail.com"
MIDDLEWARE_SK = str(os.environ.get("MIDDLEWARE_SK"))


app = FastAPI(
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    title=TITLE,
    contact={"mail": CONTACT},
)


def version_0_1_0():
    v_0_1_0 = FastAPI(
        openapi_url="/openapi.json",
        openapi_prefix="/v1",
        docs_url="/docs",
        redoc_url=None,
        title=TITLE,
        description="Twitter backend clone (FastAPI)",
        version="0.1.0",
        contact={"email": CONTACT, "name": "Bedirhan Sahin(Developer)"},
        swagger_ui_parameters={"docExpansion": "None", "syntaxHighlight.theme": "obsidian"},
        swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    )
    endpoints = [
        (r_users.router, "/users", ["users"]),
        (r_tweets.router, "/tweets", ["tweets"]),
        (r_comments.router, "/comments", ["comments"]),
        (r_follows.router, "/follow", ["follows"]),
        (r_tweet_likes.router, "/tweetLikes", ["tweet-likes"]),
        (r_comment_likes.router, "/commentLikes", ["comment-likes"]),
    ]
    v_0_1_0.include_router(r_auth.router, tags=["Auth"])

    for router, prefix, tags in endpoints:
        v_0_1_0.include_router(router, prefix=prefix, tags=tags)

    return v_0_1_0


def mount_versions():
    app.mount("/v1", version_0_1_0(), name="Version 0.1.0")


main()
