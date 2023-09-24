from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TaskModel(BaseModel):
	id: int
	created_at: datetime
	updated_at: datetime
	task_type: str
	status: str
	priority: str
	name: str
	author: int
	description: Optional[str]
	asignee: Optional[int]
	# blocks: Optional[list[int]]

	class Config:
		from_attributes = True

class TaskAddModel(BaseModel):
	task_type: str
	status: str
	priority: int
	name: str
	author: int
	description: Optional[str] = None
	asignee: Optional[int] = None


