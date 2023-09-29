from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from core.constants import TaskStatus, TaskType


class TaskDisplayModel(BaseModel):
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


class TaskDisplayModelWithLinks(TaskDisplayModel):
    linked: Optional[list[TaskDisplayModel]]
    blocking: Optional[list[TaskDisplayModel]]
    blocked_by: Optional[list[TaskDisplayModel]]


class TaskModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    task_type: TaskType
    status: TaskStatus
    priority_id: int
    name: str
    author_id: int
    description: Optional[str]
    asignee_id: Optional[int]


class TasksAsigneeStatus(BaseModel):
    asignee: Optional[int] = Field(serialization_alias="asignee_id")
    status: TaskStatus


class TaskEditModel(BaseModel):
    task_type: TaskType
    priority: int = Field(serialization_alias="priority_id")
    name: str
    author: int = Field(serialization_alias="author_id")
    description: Optional[str] = None


class TaskAddModel(TaskEditModel, TasksAsigneeStatus):
    pass
