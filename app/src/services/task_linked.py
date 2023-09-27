from fastapi import HTTPException

from core.messages import TASK_LINK_WRONG_IDS
from db.db import DBConnector
from db.task_linked import TaskLinkedAdapter
from models.task_linked import TaskLinkedAddModel


class TaskLinkedService:
    def __init__(self):
        self.conn = DBConnector(TaskLinkedAdapter)

    async def _validate_link(self, payload: TaskLinkedAddModel):
        async with self.conn as c:
            duplicate = await c.adapter.find_link(payload)
            if payload.task_id == payload.linked_id or duplicate:
                raise HTTPException(
                    400, TASK_LINK_WRONG_IDS.format(payload.task_id, payload.linked_id)
                )

    def _inverse_linked_payload(
        self, payload: TaskLinkedAddModel
    ) -> TaskLinkedAddModel:
        return TaskLinkedAddModel(linked_id=payload.task_id, task_id=payload.linked_id)

    async def link_tasks(self, payload: TaskLinkedAddModel):
        async with self.conn as c:
            await self._validate_link(payload)
            inverse_payload = self._inverse_linked_payload(payload)

            await c.adapter.add(payload.model_dump(), use_timestamp=False)
            await c.adapter.add(inverse_payload.model_dump(), use_timestamp=False)
            await c.adapter.commit()

    async def delete_link(self, payload: TaskLinkedAddModel) -> bool:
        async with self.conn as c:
            inverse_payload = self._inverse_linked_payload(payload)
            link = await c.adapter.find_link(payload)
            link_inverse = await c.adapter.find_link(inverse_payload)

            if link and link_inverse:
                await c.adapter.delete_by_id(link.id)
                await c.adapter.delete_by_id(link_inverse.id)
                await c.adapter.commit()

                return True

            return False
