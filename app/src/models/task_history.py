from datetime import datetime

from pydantic import BaseModel

from models.task import TaskAddModel


class TaskHistoryAddModel(TaskAddModel):
    updated_by_id: int
    task_id: int


class TaskHistoryModel(TaskHistoryAddModel):
    id: int
    created_at: datetime


class TaskHistoryDisplayModel(BaseModel):
    created_at: datetime
    revisions: list[TaskHistoryModel]  # TODO change to TaskHistoryAddModel
