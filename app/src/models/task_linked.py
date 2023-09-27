from pydantic import BaseModel


class TaskLinkedAddModel(BaseModel):
	task_id: int
	linked_id: int

class TaskLinkedModel(TaskLinkedAddModel):
	id: int
	task_id: int
	linked_id: int
