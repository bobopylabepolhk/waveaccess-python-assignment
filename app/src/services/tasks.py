from db.db import DBConnector
from db.tasks import TasksAdapter
from models.task import TaskAddModel


class TasksService:
    def __init__(self):
        self.conn = DBConnector(TasksAdapter)

    async def get_tasks(self):
        async with self.conn as c:
            tasks = await c.adapter.find_all()
            
            return tasks

    async def add_task(self, task: TaskAddModel):
        async with self.conn as c:
            data = task.model_dump()
            id = await c.adapter.add(data)
            await c.adapter.commit()
            
            return id
