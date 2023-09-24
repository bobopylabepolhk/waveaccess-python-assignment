from pydantic import BaseModel


class EntityId(BaseModel):
	id: int