from fastapi import (
    Depends,
    status,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param

from sqlalchemy.orm import Session

from starlette.requests import Request

from jose import JWTError

from typing import Optional

from database import SessionLocal
from security import decode_token
from cruds import c_users
from schemas import s_tokens


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def send_email_notification(username: str):
    print(f"Welcome {username}")


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": {}})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(
        self, request: Request = None, websocket: WebSocket = None
    ) -> Optional[str]:
        header_authorization: str = None
        cookie_authorization: str = None

        if request and not websocket:
            header_authorization = request.headers.get("Authorization")
            cookie_authorization = request.cookies.get("Authorization")
        elif websocket and not request:
            cookie_authorization = websocket.cookies.get("Authorization")
            header_authorization = websocket.headers.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error and request and not websocket:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
                )
            elif websocket and not request or not self.auto_error:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/v1/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    token_data: s_tokens.TokenData = None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        return None
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = s_tokens.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = c_users.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user
