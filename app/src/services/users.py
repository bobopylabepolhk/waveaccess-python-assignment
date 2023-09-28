from fastapi import HTTPException

from core.constants import UserRoles
from core.messages import USER_ALREADY_EXISTS, USER_NOT_FOUND_OR_WRONG_PASSWORD
from core.security import create_jwt, get_password_hash, verify_password
from core.settings import settings
from db.db import DBConnector
from db.users import UsersAdapter
from models.user import (
    UserDisplayModel,
    UserEditModel,
    UserLoginModel,
    UserRegisterModel,
    UserTokenModel,
)
from services.pagination import PaginationService


class UsersService:
    def __init__(self):
        self.conn = DBConnector(UsersAdapter)
        self.paginator = PaginationService(UserDisplayModel, self.conn)

    def _create_token(self, user: UserTokenModel) -> str:
        payload = user.model_dump()
        jwt = create_jwt(payload, settings.jwt_access_lifespan_minutes)

        return jwt

    async def login(self, credentials: UserLoginModel) -> str:
        async with self.conn as c:
            user = await c.adapter.get_user_by_login(credentials.login)

            if not user or not verify_password(credentials.password, user.password):
                raise HTTPException(401, USER_NOT_FOUND_OR_WRONG_PASSWORD)

            role = UserRoles(user.role).name if user.role else None

            return self._create_token(
                UserTokenModel(id=user.id, login=user.login, role=role)
            )

    async def register(self, credentials: UserRegisterModel) -> str:
        async with self.conn as c:
            user = await c.adapter.get_user_by_login(credentials.login)

            if user:
                raise HTTPException(409, USER_ALREADY_EXISTS)

            hashed_password = get_password_hash(credentials.password)
            data = {**credentials.model_dump(), "password": hashed_password}
            user_id = await c.adapter.add(data)
            await c.adapter.commit()
            role = UserRoles(credentials.role).name if credentials.role else None

            return self._create_token(
                UserTokenModel(id=user_id, login=credentials.login, role=role)
            )

    async def edit_user(self, id: int, payload: UserEditModel):
        async with self.conn as c:
            id = await c.adapter.edit_by_id(id, payload.model_dump(exclude={"id"}))
            await c.adapter.commit()

            return id
