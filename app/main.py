from fastapi import FastAPI

from routers import r_users, r_auth, r_tweets
from database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(r_users.router, prefix="/users", tags=["users"])
app.include_router(r_auth.router, tags=["Auth"])
app.include_router(r_tweets.router, prefix="/tweets", tags=["tweets"])
