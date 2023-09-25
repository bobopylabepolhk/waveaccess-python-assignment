from typing import Optional
from pydantic import BaseModel

class UserDisplayModel(BaseModel):
	id: int
	login: str
	role: Optional[str]

class UserModel(UserDisplayModel):
	password: str
	role: int
	class Config:
		from_attributes = True

class UserLoginModel(BaseModel):
	login: str
	password: str

class UserRegisterModel(UserLoginModel):
	role: Optional[int]

class UserEditModel(BaseModel):
	id: int
	login: Optional[str]
	role: Optional[int]