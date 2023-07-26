from datetime import datetime, date

from typing import List, Optional, Any
from pydantic import BaseModel, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
