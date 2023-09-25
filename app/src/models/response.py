from pydantic import BaseModel


class EntityId(BaseModel):
	id: int

class JWTResponse(BaseModel):
	access_token: str
