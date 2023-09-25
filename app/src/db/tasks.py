from datetime import datetime
from typing import Optional, Type

from fastapi import HTTPException
from core.messages import NOT_FOUND_ASIGNEE_ID
from db.users import Users
from db.base import Base
from core.constants import TaskPriority, TaskStatus, UserRoles
from db.db import DBAdapter
from models.task import TaskModel
from sqlalchemy import ForeignKey, Result, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import NoResultFound

class Tasks(Base):
	name: Mapped[str]
	created_at: Mapped[datetime]
	updated_at: Mapped[datetime]
	description: Mapped[Optional[str]]

	asignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
	author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	priority_id: Mapped[int]
	status: Mapped[Optional[str]]
	task_type: Mapped[str]


	def to_json(self) -> TaskModel:
		return TaskModel(
			id=self.id,
			name=self.name,
			asignee=self.asignee_id,
			author=self.author_id,
			created_at=self.created_at,
			updated_at=self.updated_at,
			description=self.description,
			priority=TaskPriority(self.priority_id).name,
			status=TaskStatus(self.status).name,
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
			

