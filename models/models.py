from typing import Union, Annotated
from pydantic import BaseModel, Field


class User(BaseModel):
    FirstName: Union[str, None] = None
    LastName: Union[str, None] = None
    Nickname: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None


class UserDB(User):
    password: Annotated[Union[str, None], Field(max_length=200, min_length=5)] = None


class Response(BaseModel):
    message: str
