from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
	id: int
	login: str
	role: str

	class Config:
		from_attributes = True

class UserCredentialsModel(BaseModel):
	login: str
	password: str
	role: Optional[int]

class UserEditModel(BaseModel):
	id: int
	login: Optional[str]
	role: Optional[int]