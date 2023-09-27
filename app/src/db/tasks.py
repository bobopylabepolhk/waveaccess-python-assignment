from datetime import datetime
from typing import Optional, Type

from fastapi import HTTPException
from sqlalchemy import ForeignKey, Result, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import TaskPriority, UserRoles
from core.messages import NOT_FOUND_ASIGNEE_ID
from db.base import Base
from db.db import DBAdapter
from db.task_history import TaskHistory, TaskHistoryAdapter
from db.task_linked import TaskLinked, TaskLinkedAdapter
from db.users import Users
from models.task import TaskDisplayModel, TaskModel


class Tasks(Base):
    name: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    description: Mapped[Optional[str]]

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    asignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    priority_id: Mapped[int]
    status: Mapped[str]
    task_type: Mapped[str]

    history: Mapped["TaskHistory"] = relationship(
        backref="parent", passive_deletes=True
    )
    linked: Mapped["TaskLinked"] = relationship(
        backref="parent",
        passive_deletes=True,
        primaryjoin="Tasks.id == TaskLinked.task_id",
    )

    def to_json(self) -> TaskDisplayModel:
        return TaskDisplayModel(
            id=self.id,
            name=self.name,
            asignee=self.asignee_id,
            author=self.author_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            description=self.description,
            priority=TaskPriority(self.priority_id).name,
            status=self.status,
            task_type=self.task_type,
        )


class TasksAdapter(DBAdapter):
    model: Type[Tasks] = Tasks

    async def get_asignee_role(self, asignee_id: int) -> UserRoles:
        try:
            stmt = select(Users.role).where(Users.id == asignee_id)
            res: Result = await self.session.execute(stmt)
            role = res.scalar_one()

            return role
        except NoResultFound:
            raise HTTPException(404, NOT_FOUND_ASIGNEE_ID.format(asignee_id))

    async def edit_with_history(
        self, current_user_id: int, task_id: int, data: dict, task: TaskModel
    ):
        tasks_history = TaskHistoryAdapter(self.session)

        await tasks_history.update_history(current_user_id, task_id, task)
        await self.edit_by_id(task_id, data)

    async def get_linked_tasks(self, task_id: int):
        tasks_linked = TaskLinkedAdapter(self.session)
        task_ids = await tasks_linked.get_linked_tasks_ids(task_id)
        tasks: list[TaskDisplayModel] = await self.find_by_multiple_ids(task_ids)

        return tasks
