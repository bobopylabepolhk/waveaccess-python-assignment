from typing import Annotated
from fastapi import APIRouter, Depends
from core.security import has_access
from models.response import EntityId
from models.task import TaskAddModel

from services.tasks import TasksService

TasksServiceDep = Annotated[TasksService, Depends(TasksService)]

router = APIRouter(prefix='/tasks', tags=['tasks'], dependencies=[Depends(has_access)])

@router.get('/')
async def get_tasks(
    tasks_service: TasksServiceDep,
):
    tasks = await tasks_service.get_tasks()

    return tasks

@router.post('/')
async def add_task(
    task: TaskAddModel,
    tasks_service: TasksServiceDep,
):
    task_id = await tasks_service.add_task(task)

    return EntityId(id=task_id)
