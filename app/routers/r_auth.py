from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2

from starlette.responses import Response

from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from security import authenticate_user, create_access_token
from schemas import s_users


router = APIRouter(tags=["Auth"])


@router.post("/token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
        samesite="Lax",
        domain="localhost",
        httponly=True,
        max_age=60 * 30,
        expires=60 * 30,
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout_and_expire_cookie(
    response: Response, current_user: s_users.User = Depends(get_current_user)
):
    response.set_cookie(
        key="Authorization",
        value="",
        samesite="Lax",
        domain="localhost",
        httponly=True,
        max_age=1,
        expires=-1,
    )
    return {}
