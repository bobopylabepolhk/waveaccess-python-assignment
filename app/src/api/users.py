from typing import Annotated
from fastapi import APIRouter, Depends
from models.response import EntityId
from models.user import UserCredentialsModel, UserEditModel
from services.users import UsersService

UsersServiceDep = Annotated[UsersService, Depends(UsersService)]

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.get('/')
async def get_users(users_service: UsersServiceDep):
    tasks = await users_service.get_users()

    return tasks

@router.post('/login')
async def login(credentials: UserCredentialsModel, users_service: UsersServiceDep):
    # TODO
    pass

@router.post('/register')
async def register(
    credentials: UserCredentialsModel, 
    users_service: UsersServiceDep
):
    # WIP
    # TODO login()
    user_id = await users_service.register(credentials)

    return EntityId(id=user_id)


@router.patch('/edit')
async def edit_user(payload: UserEditModel, users_service: UsersServiceDep):
    user_id = await users_service.edit_user(payload)

    return EntityId(id=user_id)
