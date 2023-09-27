from datetime import datetime
from typing import Optional, Type

from sqlalchemy import ForeignKey, Result, select
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.db import DBAdapter
from models.task import TaskModel
from models.task_history import TaskHistoryAddModel, TaskHistoryModel


class TaskHistory(Base):
    name: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    description: Mapped[Optional[str]]

    asignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    priority_id: Mapped[int]
    status: Mapped[str]
    task_type: Mapped[str]

    updated_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))

    def to_json(self) -> TaskHistoryModel:
        return TaskHistoryModel(
            id=self.id,
            asignee=self.asignee_id,
            author=self.author_id,
            created_at=self.created_at,
            description=self.description,
            name=self.name,
            priority=self.priority_id,
            status=self.status,
            task_id=self.task_id,
            task_type=self.task_type,
            updated_by_id=self.updated_by_id,
        )


class TaskHistoryAdapter(DBAdapter):
    model: Type[TaskHistory] = TaskHistory

    async def get_all_history_records(self, task_id: int) -> list[TaskHistoryModel]:
        stmt = (
            select(self.model)
            .where(self.model.task_id == task_id)
            .order_by(self.model.created_at)
        )
        res: Result = await self.session.execute(stmt)

        return [row.to_json() for row in res.scalars().all()]

    async def update_history(self, user_id: int, task_id: int, task: TaskModel):
        history_record = TaskHistoryAddModel(
            updated_by_id=user_id,
            task_id=task_id,
            asignee=task.asignee_id,
            author=task.author_id,
            status=task.status,
            task_type=task.task_type,
            priority=task.priority_id,
            name=task.name,
            description=task.description,
        )
        data = history_record.model_dump(by_alias=True)
        await self.add(data)
