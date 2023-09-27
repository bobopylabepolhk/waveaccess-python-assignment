from datetime import datetime
from typing import  Generic, Type, TypeVar
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import Result
from core.messages import DEFAULT_404_MESSAGE
from db.base import Base
from core.settings import settings

''' ORM Adapter '''

TK = TypeVar('TK')
class DBAdapter(Generic[TK]):
	model: Type[Base]

	def __init__(self, session: AsyncSession):
		self.session = session
	
	@staticmethod
	def _add_initial_timestamps(data: dict):
		created_at = datetime.utcnow()

		return { **data, 'created_at': created_at, 'updated_at': created_at }
	
	@staticmethod
	def _update_timestamp(data: dict):
		updated_at = datetime.utcnow()

		return { **data, 'updated_at': updated_at }

	async def commit(self):
		await self.session.commit()
	
	async def find_all(self) -> list[TK]:
		stmt = select(self.model)
		res: Result = await self.session.execute(stmt)
	
		return [row.to_json() for row in res.scalars().all()]
	
	async def find_by_id(self, id: int) -> TK | None:
		stmt = select(self.model).where(self.model.id == id)
		res: Result = await self.session.execute(stmt)
	
		return res.scalar_one_or_none()
	
	async def find_by_multiple_ids(self, ids: list[int]) -> list[TK]:
		stmt = select(self.model).where(self.model.id.in_(ids))
		res: Result = await self.session.execute(stmt)

		return [row.to_json() for row in res.scalars().all()]
	
	async def find_by_id_or_404(self, id: int, error_msg: str = DEFAULT_404_MESSAGE) -> TK:
		res = await self.find_by_id(id)

		if not res:
			raise HTTPException(404, error_msg)
		
		return res

	async def add(self, data: dict, use_timestamp: bool = True) -> int:
		data = self._add_initial_timestamps(data) if use_timestamp else data
		stmt = insert(self.model).values(**data).returning(self.model.id)
		res = await self.session.execute(stmt)

		return res.scalar_one()
	
	async def edit_by_id(self, id: int, data: dict):
		data_with_timestamp = self._update_timestamp(data)
		stmt = update(self.model).values(**data_with_timestamp).filter_by(id=id)
		await self.session.execute(stmt)
	
	async def delete_by_id(self, id: int) -> bool:
		stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
		res: Result = await self.session.execute(stmt)

		return bool(res.scalar_one_or_none())

''' prepare postgres connection '''

engine = create_async_engine(settings.get_pg_conn_str())
get_session = async_sessionmaker(engine, expire_on_commit=False)

T = TypeVar('T')
class DBConnector(Generic[T]):
	def __init__(self, adapter: Type[T]):
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