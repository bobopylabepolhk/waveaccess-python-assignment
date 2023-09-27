from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


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


class TasksAsigneeStatus(BaseModel):
    asignee: Optional[int] = Field(serialization_alias="asignee_id")
    status: str


class TaskEditModel(BaseModel):
    task_type: str
    priority: int = Field(serialization_alias="priority_id")
    name: str
    author: int = Field(serialization_alias="author_id")
    description: Optional[str] = None


class TaskAddModel(TaskEditModel, TasksAsigneeStatus):
    pass
