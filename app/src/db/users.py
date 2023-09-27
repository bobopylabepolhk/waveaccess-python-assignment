from datetime import datetime
from typing import Type

from sqlalchemy import Result, select
from sqlalchemy.orm import Mapped

from core.constants import UserRoles
from db.base import Base
from db.db import DBAdapter
from models.user import UserDisplayModel, UserModel


class Users(Base):
    login: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    password: Mapped[str]
    role: Mapped[int]

    def to_json(self) -> UserDisplayModel:
        return UserDisplayModel(
            id=self.id, login=self.login, role=UserRoles(self.role).name
        )


class UsersAdapter(DBAdapter):
    model: Type[Users] = Users

    async def get_user_by_login(self, login: str) -> UserModel | None:
        stmt = select(self.model).where(self.model.login == login)
        res: Result = await self.session.execute(stmt)

        return res.scalar_one_or_none()
