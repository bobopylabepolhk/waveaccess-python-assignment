from typing import Type

from sqlalchemy import ForeignKey, Result, and_, select
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.db import DBAdapter
from models.task_linked import TaskLinkedAddModel, TaskLinkedModel


class TaskLinked(Base):
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    linked_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))

    def to_json(self) -> TaskLinkedModel:
        return TaskLinkedModel(
            id=self.id, task_id=self.task_id, linked_id=self.linked_id
        )


class TaskLinkedAdapter(DBAdapter):
    model: Type[TaskLinked] = TaskLinked

    async def find_link(self, payload: TaskLinkedAddModel) -> TaskLinkedModel | None:
        stmt = select(self.model).where(
            and_(
                self.model.task_id == payload.task_id,
                self.model.linked_id == payload.linked_id,
            )
        )
        res: Result = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def get_linked_tasks_ids(self, task_id: int) -> list[int]:
        stmt = select(self.model).where(self.model.task_id == task_id)
        res: Result = await self.session.execute(stmt)
        tasks_linked_ids = [
            task_linked_row.to_json().linked_id
            for task_linked_row in res.scalars().all()
        ]

        return tasks_linked_ids
