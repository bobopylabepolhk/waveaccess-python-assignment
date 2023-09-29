from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from api.dependencies import has_role_dep
from core.constants import DEFAULT_PER_PAGE, SortOrder, UserRoles
from models.response import EntityId, JWTResponse
from models.user import (
    UserDisplayModel,
    UserEditModel,
    UserLoginModel,
    UserRegisterModel,
)
from services.users import UsersService

UsersServiceDep = Annotated[UsersService, Depends(UsersService)]

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserDisplayModel])
async def get_users(
    users_service: UsersServiceDep,
    sort: str = UsersService.DEFAULT_SORT_KEY,
    sort_order: Optional[SortOrder] = UsersService.DEFAULT_SORT_ORDER,
    page: int = 1,
    per_page: int = DEFAULT_PER_PAGE,
):
    users = await users_service.paginator.get_paginated(
        sort=sort,
        sort_order=sort_order,
        per_page=per_page,
        page=page,
    )

    return users


@router.post("/login", response_model=JWTResponse)
async def login(credentials: UserLoginModel, users_service: UsersServiceDep):
    token = await users_service.login(credentials)

    return JWTResponse(access_token=token)


@router.post("/register", response_model=JWTResponse)
async def register(credentials: UserRegisterModel, users_service: UsersServiceDep):
    token = await users_service.register(credentials)

    return JWTResponse(access_token=token)


@router.patch(
    "/{user_id}",
    dependencies=[has_role_dep(UserRoles.MANAGER)],
    response_model=EntityId,
    summary="Edit user login or role. Requires role MANAGER",
)
async def edit_user(
    user_id: int, payload: UserEditModel, users_service: UsersServiceDep
):
    id = await users_service.edit_user(user_id, payload)

    return EntityId(id=id)
