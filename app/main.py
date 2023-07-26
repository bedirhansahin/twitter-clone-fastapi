from fastapi import FastAPI

from routers import r_users
from database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(r_users.router)
