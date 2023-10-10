from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.constants import UserRoles


class UserDisplayModel(BaseModel):
    id: int
    login: str
    role: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserModel(UserDisplayModel):
    password: str
    role: int


class UserLoginModel(BaseModel):
    login: str
    password: str


class UserRegisterModel(UserLoginModel):
    role: UserRoles


class UserTokenModel(BaseModel):
    id: int
    login: str
    role: str


class UserEditModel(BaseModel):
    login: Optional[str]
    role: Optional[int]
