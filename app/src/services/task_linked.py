from fastapi import HTTPException
from core.messages import TASK_LINK_WRONG_IDS
from models.task_linked import TaskLinkedAddModel
from db.db import DBConnector
from db.task_linked import TaskLinkedAdapter


class TaskLinkedService:
	def __init__(self):
		self.conn = DBConnector(TaskLinkedAdapter)

	async def _validate_link(self, payload: TaskLinkedAddModel):
		async with self.conn as c:
			duplicate = await c.adapter.find_link(payload)
			if payload.task_id == payload.linked_id or duplicate:
				raise HTTPException(400, TASK_LINK_WRONG_IDS.format(payload.task_id, payload.linked_id))
	
	async def link_tasks(self, payload: TaskLinkedAddModel):
		async with self.conn as c:
			await self._validate_link(payload)
			data = payload.model_dump()
			
			id = await c.adapter.add(data, use_timestamp=False)
			await c.adapter.commit()

			return id
		
	async def delete_link(self, payload: TaskLinkedAddModel):
		async with self.conn as c:
			link = await c.adapter.find_link(payload)

			if not link:
				return False

			is_deleted = await c.adapter.delete_by_id(link.id)
			await c.adapter.commit()

			return is_deleted
