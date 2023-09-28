from datetime import datetime
from math import ceil
from typing import Generic, Tuple, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import Select, asc, delete, desc, func, insert, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.constants import SortOrder
from core.messages import DEFAULT_404_MESSAGE
from core.settings import settings
from db.base import Base
from models.pagination import PaginationResponseModel

""" ORM Adapter """

Model = TypeVar("Model")


class DBAdapter(Generic[Model]):
    model: Type[Base]

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _add_initial_timestamps(data: dict):
        created_at = datetime.utcnow()

        return {**data, "created_at": created_at, "updated_at": created_at}

    @staticmethod
    def _update_timestamp(data: dict):
        updated_at = datetime.utcnow()

        return {**data, "updated_at": updated_at}

    async def _count_total_items(self, query: Select[Tuple[Base]]) -> int | None:
        stmt = query.with_only_columns(func.count(self.model.id)).order_by(None)
        res: Result = await self.session.execute(stmt)

        return res.scalar()

    async def commit(self):
        await self.session.commit()

    async def find_all(self) -> list[Model]:
        stmt = select(self.model)
        res: Result = await self.session.execute(stmt)

        return [row.to_json() for row in res.scalars().all()]

    async def find_all_with_sort(self, sort: str, sort_order: SortOrder):
        order = asc if sort_order == SortOrder.ASC else desc
        stmt = select(self.model).order_by(order(sort))
        res: Result = await self.session.execute(stmt)

        return [row.to_json() for row in res.scalars().all()]

    async def find_all_with_pagination(
        self, sort: str, sort_order: SortOrder, per_page: int, page: int
    ) -> PaginationResponseModel:
        order = asc if sort_order == SortOrder.ASC else desc
        limit = per_page * page
        offset = (page - 1) * per_page

        stmt = select(self.model).order_by(order(sort)).limit(limit).offset(offset)
        total_items = await self._count_total_items(stmt)
        total_pages = ceil(total_items / per_page)
        res: Result = await self.session.execute(stmt)
        data = [row.to_json() for row in res.scalars().all()]

        return PaginationResponseModel(
            data=data,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_items=total_items,
        )

    async def find_by_id(self, id: int) -> Model | None:
        stmt = select(self.model).where(self.model.id == id)
        res: Result = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def find_by_multiple_ids(self, ids: list[int]) -> list[Model]:
        stmt = select(self.model).where(self.model.id.in_(ids))
        res: Result = await self.session.execute(stmt)

        return [row.to_json() for row in res.scalars().all()]

    async def find_by_id_or_404(
        self, id: int, error_msg: str = DEFAULT_404_MESSAGE
    ) -> Model:
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


""" prepare postgres connection """

engine = create_async_engine(settings.get_pg_conn_str())
get_session = async_sessionmaker(engine, expire_on_commit=False)

Adapter = TypeVar("Adapter")


class DBConnector(Generic[Adapter]):
    def __init__(self, adapter: Type[Adapter]):
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
