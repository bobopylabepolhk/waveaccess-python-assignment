from datetime import datetime
from typing import Optional
from db.base import Base
from core.constants import TaskPriority, TaskStatus
from db.db import DBAdapter
from models.task import TaskModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


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
	model = Tasks

