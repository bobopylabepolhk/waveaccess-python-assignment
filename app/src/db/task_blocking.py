from typing import Type

from sqlalchemy import ForeignKey, Result, and_, select
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.db import DBAdapter
from models.task_blocking import TaskBlockingAddModel, TaskBlockingModel


class TaskBlocking(Base):
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    blocking_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))

    def to_json(self) -> TaskBlockingModel:
        return TaskBlockingModel(
            id=self.id, task_id=self.task_id, blocking_id=self.blocking_id
        )


class TaskBlockingAdapter(DBAdapter):
    model: Type[TaskBlocking] = TaskBlocking

    async def get_blocking_ids(self, id: int) -> tuple[list[int], list[int]]:
        blocked_by_stmt = select(self.model).where(self.model.blocking_id == id)
        blocking_stmt = select(self.model).where(self.model.task_id == id)
        blocked_by_res: Result = await self.session.execute(blocked_by_stmt)
        blocking_res: Result = await self.session.execute(blocking_stmt)

        blocked_by_ids = [
            task.to_json().task_id for task in blocked_by_res.scalars().all()
        ]

        blocking_ids = [
            task.to_json().blocking_id for task in blocking_res.scalars().all()
        ]

        return (blocked_by_ids, blocking_ids)

    async def find_blocking(
        self, payload: TaskBlockingAddModel
    ) -> TaskBlockingModel | None:
        stmt = select(self.model).where(
            and_(
                self.model.task_id == payload.task_id,
                self.model.blocking_id == payload.blocking_id,
            )
        )
        res: Result = await self.session.execute(stmt)

        return res.scalar_one_or_none()
