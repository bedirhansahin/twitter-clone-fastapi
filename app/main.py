from fastapi import FastAPI

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from routers import r_users, r_auth, r_tweets
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
        version="0.1.0",
        contact={"mail": CONTACT},
        swagger_ui_parameters={"docExpansion": "None"},
    )
    endpoints = [
        (r_users.router, "/users", ["users"]),
        (r_tweets.router, "/tweets", ["tweets"]),
    ]
    v_0_1_0.include_router(r_auth.router, tags=["Auth"])

    for router, prefix, tags in endpoints:
        v_0_1_0.include_router(router, prefix=prefix, tags=tags)

    return v_0_1_0


def mount_versions():
    app.mount("/v1", version_0_1_0(), name="Version 0.1.0")


main()
