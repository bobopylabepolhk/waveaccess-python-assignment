from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserDisplayModel(BaseModel):
	id: int
	login: str
	role: Optional[str]

class UserModel(UserDisplayModel):
	password: str
	role: int
	created_at: datetime
	updated_at: datetime

class UserLoginModel(BaseModel):
	login: str
	password: str

class UserRegisterModel(UserLoginModel):
	role: Optional[int]

class UserEditModel(BaseModel):
	login: Optional[str]
	role: Optional[int]