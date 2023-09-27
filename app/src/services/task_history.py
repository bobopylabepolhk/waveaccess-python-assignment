from datetime import datetime
from models.task_history import TaskHistoryDisplayModel, TaskHistoryModel
from db.db import DBConnector
from db.task_history import TaskHistoryAdapter


class TaskHistoryService:
	def __init__(self):
		self.conn = DBConnector(TaskHistoryAdapter)

	async def get_history(self, task_id: int) -> list[TaskHistoryDisplayModel]:
		async with self.conn as c:
			history_records = await c.adapter.get_all_history_records(task_id)
			history_records_by_timestamp: dict[datetime, list[TaskHistoryModel]] = {}
			res: list[TaskHistoryDisplayModel] = []

			for record in history_records:
				if record.created_at in history_records_by_timestamp:
					history_records_by_timestamp[record.created_at].append(record)
				else:
					history_records_by_timestamp[record.created_at] = [record]
			
			for created_at, record in history_records_by_timestamp.items():
				data = TaskHistoryDisplayModel(created_at=created_at, revisions=record)
				res.append(data)
			
			return res
			
			
				
				
			

