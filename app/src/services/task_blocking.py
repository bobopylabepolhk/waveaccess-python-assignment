from db.db import DBConnector
from db.task_blocking import TaskBlockingAdapter
from models.task_linked import TaskLinkedAddModel


class TaskBlockingService:
    def __init__(self):
        self.conn = DBConnector(TaskBlockingAdapter)

    async def add_blocking(self, payload: TaskLinkedAddModel):
        async with self.conn as c:
            await c.adapter.add(payload.model_dump(), use_timestamp=False)
            await c.adapter.commit()

    async def delete_blocking(self, payload: TaskLinkedAddModel) -> bool:
        async with self.conn as c:
            blocking = await c.adapter.find_blocking(payload)

            if blocking:
                await c.adapter.delete_by_id(blocking.id)
                await c.adapter.commit()

                return True

            return False
