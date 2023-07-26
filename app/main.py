from fastapi import FastAPI

from routers import r_users, r_auth
from database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(r_users.router)
app.include_router(r_auth.router)
