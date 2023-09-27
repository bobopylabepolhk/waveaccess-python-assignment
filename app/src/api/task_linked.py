from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import has_access_dep
from models.response import EntityId

from models.task_linked import TaskLinkedAddModel
from services.task_linked import TaskLinkedService

TasksLinkedServiceDep = Annotated[TaskLinkedService, Depends(TaskLinkedService)]

router = APIRouter(prefix='/tasks-linked', tags=['tasks-linked'])

@router.post('/link', dependencies=[has_access_dep])
async def link_tasks(
    payload: TaskLinkedAddModel,
    tasks_linked_service: TasksLinkedServiceDep
):
    id = await tasks_linked_service.link_tasks(payload)

    return EntityId(id=id)

@router.delete('/link', dependencies=[has_access_dep])
async def delete_link(
    payload: TaskLinkedAddModel,
    tasks_linked_service: TasksLinkedServiceDep
):
    is_deleted = await tasks_linked_service.delete_link(payload)

    if is_deleted:
        return status.HTTP_200_OK
    
    return status.HTTP_304_NOT_MODIFIED
