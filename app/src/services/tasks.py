from fastapi import HTTPException

from core.constants import TaskPriority, TaskStatus, UserRoles
from core.messages import (
    TASK_INVALID_ASIGNEE_ROLE,
    TASK_INVALID_STATUS_CHAIN,
    TASK_INVALID_STATUS_IN_PROGRESS,
    TASK_NOT_FOUND_BY_ID,
    TASK_STATUS_DOES_NOT_EXIST,
)
from db.db import DBConnector
from db.tasks import Tasks, TasksAdapter
from models.task import (
    TaskAddModel,
    TaskDisplayModel,
    TaskDisplayModelWithLinks,
    TaskEditModel,
    TaskModel,
    TasksAsigneeStatus,
)
from services.pagination import PaginationService


class TasksService:
    def __init__(self):
        self.conn = DBConnector(TasksAdapter)
        self.paginator = PaginationService(TaskDisplayModel, self.conn)
        self._status_chain = [e for e in TaskStatus]

    def _validate_task_status(self, old_status: TaskStatus, new_status: TaskStatus):
        try:
            old_status_idx = self._status_chain.index(old_status)
            new_status_idx = self._status_chain.index(new_status)
            status_step = abs(new_status_idx - old_status_idx)

            if status_step > 1:
                bug_found_flow = (
                    old_status == TaskStatus.DEV_TEST
                    or old_status == TaskStatus.TESTING
                ) and new_status == TaskStatus.IN_PROGRESS
                todo_or_wontfix = (
                    new_status == TaskStatus.TODO or new_status == TaskStatus.WONT_FIX
                )

                if not bug_found_flow and not todo_or_wontfix:
                    raise HTTPException(
                        400, TASK_INVALID_STATUS_CHAIN.format(old_status, new_status)
                    )
        except ValueError:
            raise HTTPException(400, TASK_STATUS_DOES_NOT_EXIST.format(new_status))

    async def _validate_task_asignee(self, payload: TasksAsigneeStatus):
        task_status = payload.status
        allowed_status_by_role = {
            UserRoles.TEAM_LEAD: self._status_chain,
            UserRoles.DEV: [
                TaskStatus.TODO,
                TaskStatus.IN_PROGRESS,
                TaskStatus.CODE_REVIEW,
                TaskStatus.DEV_TEST,
                TaskStatus.DONE,
                TaskStatus.WONT_FIX,
            ],
            UserRoles.MANAGER: [],
            UserRoles.QA: [
                TaskStatus.TODO,
                TaskStatus.TESTING,
                TaskStatus.DONE,
                TaskStatus.WONT_FIX,
            ],
        }

        async with self.conn as c:
            if payload.asignee:
                asignee_role = await c.adapter.get_asignee_role(payload.asignee)

                if task_status not in allowed_status_by_role[asignee_role]:
                    raise HTTPException(
                        400, TASK_INVALID_ASIGNEE_ROLE.format(task_status, asignee_role)
                    )

            elif task_status == TaskStatus.IN_PROGRESS:
                raise HTTPException(400, TASK_INVALID_STATUS_IN_PROGRESS)

    async def get_task_by_id(self, id: int) -> TaskDisplayModelWithLinks | None:
        async with self.conn as c:
            task: Tasks = await c.adapter.find_by_id_or_404(id)
            linked: list[TaskDisplayModel] = await c.adapter.get_linked_tasks(id)

            return TaskDisplayModelWithLinks(
                id=task.id,
                author=task.author_id,
                created_at=task.created_at,
                asignee=task.asignee_id,
                description=task.description,
                name=task.name,
                priority=TaskPriority(task.priority_id).name,
                status=task.status,
                task_type=task.task_type,
                updated_at=task.updated_at,
                linked=linked,
            )

    async def add_task(self, task: TaskAddModel) -> int:
        async with self.conn as c:
            await self._validate_task_asignee(task)
            data = task.model_dump(by_alias=True)
            id = await c.adapter.add(data)
            await c.adapter.commit()

            return id

    async def edit_task(self, current_user_id: int, id: int, payload: TaskEditModel):
        async with self.conn as c:
            task = await c.adapter.find_by_id_or_404(id)

            data = payload.model_dump(by_alias=True)
            await c.adapter.edit_with_history(current_user_id, id, data, task)
            await c.adapter.commit()

    async def edit_status_asignee(
        self, current_user_id: int, id: int, payload: TasksAsigneeStatus
    ):
        async with self.conn as c:
            await self._validate_task_asignee(payload)

            task: TaskModel = await c.adapter.find_by_id_or_404(id)

            self._validate_task_status(
                TaskStatus[task.status], TaskStatus[payload.status]
            )
            data = payload.model_dump(by_alias=True)
            await c.adapter.edit_with_history(current_user_id, id, data, task)
            await c.adapter.commit()

    async def delete_task(self, id: int):
        async with self.conn as c:
            is_deleted = await c.adapter.delete_by_id(id)

            if not is_deleted:
                raise HTTPException(404, TASK_NOT_FOUND_BY_ID.format(id))

            await c.adapter.commit()
