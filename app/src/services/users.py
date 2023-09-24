from db.db import DBConnector
from utils.extract_id_from_model_dump import extract_id_from_model_dump
from db.users import UsersAdapter
from models.user import UserCredentialsModel, UserEditModel


class UsersService:
	def __init__(self):
		self.conn = DBConnector(UsersAdapter)
	
	async def get_users(self):
		async with self.conn as c:
			users = await c.adapter.find_all()

			return users
	
	async def login(self, credentials: UserCredentialsModel):
		# WIP DRAFT
		# TODO issue tokens; send tokens
		pass
	
	async def register(self, credentials: UserCredentialsModel) -> int:
		# WIP DRAFT
		# TODO login + password validation; save password hash; return status: OK
		async with self.conn as c:
			data = credentials.model_dump()
			id = await c.adapter.add(data)
			await c.adapter.commit()

			return id

	async def edit_user(self, payload: UserEditModel):
		async with self.conn as c:
			user_id, data = extract_id_from_model_dump(payload.model_dump())
			id = await c.adapter.edit_by_id(user_id, data)
			await c.adapter.commit()
			
			return id