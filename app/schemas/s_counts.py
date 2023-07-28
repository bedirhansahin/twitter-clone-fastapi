from pydantic import BaseModel


class CountBase(BaseModel):
    count: int
