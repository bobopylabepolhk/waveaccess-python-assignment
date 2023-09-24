from core.constants import UserRoles
from db.db import DBAdapter
from db.base import Base
from sqlalchemy.orm import Mapped

from models.user import UserModel


class Users(Base):
	login: Mapped[str]
	password: Mapped[str]
	role: Mapped[int]

	def to_json(self) -> UserModel:
		return UserModel(
			id=self.id,
			login=self.login,
			role=UserRoles(self.role).name
		)

class UsersAdapter(DBAdapter):
	model = Users

