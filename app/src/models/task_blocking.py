from pydantic import BaseModel


class TaskBlockingAddModel(BaseModel):
    task_id: int
    blocking_id: int


class TaskBlockingModel(TaskBlockingAddModel):
    id: int
