from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dependencies import current_user_id_dep, has_access_dep, has_role_dep
from core.constants import (
    DEFAULT_PER_PAGE,
    DEFAULT_SORT_KEY,
    DEFAULT_SORT_ORDER,
    SortOrder,
    UserRoles,
)
from models.pagination import PaginationResponseModel
from models.response import EntityId
from models.task import (
    TaskAddModel,
    TaskDisplayModelWithLinks,
    TaskEditModel,
    TasksAsigneeStatus,
)
from models.task_linked import TaskLinkedAddModel
from services.task_history import TaskHistoryService
from services.task_linked import TaskLinkedService
from services.tasks import TasksService

TasksServiceDep = Annotated[TasksService, Depends(TasksService)]
TaskHistoryServiceDep = Annotated[TaskHistoryService, Depends(TaskHistoryService)]
TasksLinkedServiceDep = Annotated[TaskLinkedService, Depends(TaskLinkedService)]

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", dependencies=[has_access_dep], response_model=PaginationResponseModel)
async def get_tasks(
    tasks_service: TasksServiceDep,
    sort: str = DEFAULT_SORT_KEY,
    page: int = 1,
    per_page: int = DEFAULT_PER_PAGE,
    sort_order: SortOrder | None = DEFAULT_SORT_ORDER,
):
    tasks = await tasks_service.paginator.get_paginated(
        sort, sort_order, per_page, page
    )

    return tasks


@router.get(
    "/{task_id}",
    dependencies=[has_access_dep],
    response_model=TaskDisplayModelWithLinks,
)
async def get_task_by_id(
    task_id: int,
    tasks_service: TasksServiceDep,
):
    task = await tasks_service.get_task_by_id(task_id)

    return task


@router.post("/", dependencies=[has_access_dep], response_model=EntityId)
async def add_task(
    task: TaskAddModel,
    tasks_service: TasksServiceDep,
):
    task_id = await tasks_service.add_task(task)

    return EntityId(id=task_id)


@router.patch("/{task_id}")
async def edit_task(
    task_id: int,
    task: TaskEditModel,
    tasks_service: TasksServiceDep,
    current_user_id: current_user_id_dep,
):
    await tasks_service.edit_task(current_user_id, task_id, task)

    return status.HTTP_200_OK


@router.patch("/{task_id}/status_asignee", summary="Edit task status or asignee")
async def edit_task_asignee_status(
    task_id: int,
    asignee_status: TasksAsigneeStatus,
    tasks_service: TasksServiceDep,
    current_user_id: current_user_id_dep,
):
    await tasks_service.edit_status_asignee(current_user_id, task_id, asignee_status)

    return status.HTTP_200_OK


@router.delete("/{task_id}/delete", dependencies=[has_role_dep(UserRoles.MANAGER)])
async def delete_task(task_id: int, tasks_service: TasksServiceDep):
    await tasks_service.delete_task(task_id)

    return status.HTTP_200_OK


""" history """


@router.get("/{task_id}/history")
async def get_task_history(task_id: int, task_history_service: TaskHistoryServiceDep):
    task_history = await task_history_service.get_history(task_id)

    return task_history


""" linked tasks """


@router.post("/link", dependencies=[has_access_dep])
async def link_tasks(
    payload: TaskLinkedAddModel, tasks_linked_service: TasksLinkedServiceDep
):
    await tasks_linked_service.link_tasks(payload)

    return status.HTTP_200_OK


@router.delete("/link", dependencies=[has_access_dep], summary="Unlink tasks")
async def delete_link(
    payload: TaskLinkedAddModel, tasks_linked_service: TasksLinkedServiceDep
):
    is_deleted = await tasks_linked_service.delete_link(payload)

    if is_deleted:
        return status.HTTP_200_OK
