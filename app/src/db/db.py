from typing import  Type
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import insert, select, update
from sqlalchemy.engine import Result
from db.base import Base
from core.settings import get_pg_conn_str

''' ORM Adapter '''

class DBAdapter:
	model: Type[Base]

	def __init__(self, session: AsyncSession):
		self.session = session

	async def commit(self):
		await self.session.commit()
	
	async def find_all(self):
		stmt = select(self.model)
		res: Result = await self.session.execute(stmt)
	
		return [row.to_json() for row in res.scalars().all()]
	
	async def find_by_id(self, id: int):
		return await self.session.get(self.model, id)

	async def add(self, data: dict) -> int:
		stmt = insert(self.model).values(**data).returning(self.model.id)
		res = await self.session.execute(stmt)
		await self.session.flush()

		return res.scalar_one()
	
	async def edit_by_id(self, id: int, data: dict) -> int:
		stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
		res = await self.session.execute(stmt)

		return res.scalar_one()
			

''' prepare postgres connection '''

engine = create_async_engine(get_pg_conn_str())
get_session = async_sessionmaker(engine, expire_on_commit=False)

class DBConnector:
	def __init__(self, adapter: Type[DBAdapter]):
		self._adapter = adapter

	async def __aenter__(self):
		self._session = get_session()
		self.adapter = self._adapter(self._session)

		return self

	async def __aexit__(self, *args):
		await self.rollback()
		await self._session.close()

	async def commit(self):
		await self._session.commit()

	async def rollback(self):
		await self._session.rollback()