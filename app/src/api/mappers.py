from fastapi import APIRouter

from core.constants import TaskPriority, TaskStatus, TaskType, UserRoles
from utils.enum_to_dict import enum_to_dict

router = APIRouter(prefix="/mappers", tags=["mappers"])


@router.get("/task-priority")
def get_task_priority():
    return enum_to_dict(TaskPriority)


@router.get("/task-type")
def get_task_type():
    return enum_to_dict(TaskType)


@router.get("/task-status")
def get_task_status():
    return enum_to_dict(TaskStatus)


@router.get("/user-roles")
def get_user_roles():
    return enum_to_dict(UserRoles)
