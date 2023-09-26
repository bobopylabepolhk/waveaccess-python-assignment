from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import has_access_dep, has_role_dep
from core.constants import UserRoles
from models.response import EntityId
from models.task import TaskAddModel

from services.tasks import TasksService

TasksServiceDep = Annotated[TasksService, Depends(TasksService)]

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/', dependencies=[has_access_dep])
async def get_tasks(
    tasks_service: TasksServiceDep,
):
    tasks = await tasks_service.get_tasks()

    return tasks

@router.get('/{task_id}', dependencies=[has_access_dep])
async def get_task_by_id(
    task_id: int,
    tasks_service: TasksServiceDep,
):
    tasks = await tasks_service.get_task_by_id(task_id)

    return tasks

@router.post('/', dependencies=[has_access_dep])
async def add_task(
    task: TaskAddModel,
    tasks_service: TasksServiceDep,
):
    task_id = await tasks_service.add_task(task)

    return EntityId(id=task_id)

@router.patch('/{task_id}', dependencies=[has_access_dep])
async def edit_task(
    task_id: int,
    task: TaskAddModel,
    tasks_service: TasksServiceDep,
):
    await tasks_service.edit_task(task_id, task)

    return status.HTTP_200_OK

@router.delete('/{task_id}', dependencies=[has_role_dep(UserRoles.MANAGER)])
async def delete_task(
    task_id: int,
    tasks_service: TasksServiceDep
):
    await tasks_service.delete_task(task_id)

    return status.HTTP_200_OK