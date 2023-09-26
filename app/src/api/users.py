from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import has_role_dep
from core.constants import UserRoles
from models.response import JWTResponse
from models.user import UserRegisterModel, UserLoginModel, UserEditModel
from services.users import UsersService

UsersServiceDep = Annotated[UsersService, Depends(UsersService)]

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.get('/')
async def get_users(users_service: UsersServiceDep):
    tasks = await users_service.get_users()

    return tasks

@router.post('/login')
async def login(credentials: UserLoginModel, users_service: UsersServiceDep):
    token = await users_service.login(credentials)

    return JWTResponse(access_token=token)

@router.post('/register')
async def register(
    credentials: UserRegisterModel, 
    users_service: UsersServiceDep
):
    token = await users_service.register(credentials)

    return JWTResponse(access_token=token)

@router.patch('/edit', dependencies=[has_role_dep(UserRoles.MANAGER)])
async def edit_user(payload: UserEditModel, users_service: UsersServiceDep):
    await users_service.edit_user(payload)

    return status.HTTP_200_OK
