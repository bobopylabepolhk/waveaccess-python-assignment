from typing import Annotated

from fastapi import APIRouter, Depends

from services.task_history import TaskHistoryService

TaskHistoryServiceDep = Annotated[TaskHistoryService, Depends(TaskHistoryService)]


router = APIRouter(
    prefix="/task_history",
    tags=["task history"],
)


@router.get("/{task_id}")
async def get_task_history(task_id: int, task_history_service: TaskHistoryServiceDep):
    task_history = await task_history_service.get_history(task_id)

    return task_history
