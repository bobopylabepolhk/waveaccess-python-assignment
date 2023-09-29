from typing import Optional

from fastapi import HTTPException

from core.constants import SortOrder
from core.messages import INVALID_SORT_PARAM
from db.db import DBConnector
from models.pagination import PaginationResponseModel


class PaginationService:
    def __init__(
        self,
        conn: DBConnector,
        default_sort_key: str,
        avaliable_sort_keys: [str],
        default_sort_order: Optional[SortOrder] = SortOrder.DESC,
    ):
        self.conn = conn
        self.default_sort_key = default_sort_key
        self.default_sort_order = default_sort_order
        self.avaliable_sort_keys = avaliable_sort_keys

    def _validate_sort_key(self, sort: str):
        if sort not in self.avaliable_sort_keys:
            sort_keys_str = " ".join(self.avaliable_sort_keys)
            raise HTTPException(400, INVALID_SORT_PARAM.format(sort, sort_keys_str))

    async def get_sorted(
        self, sort: Optional[str], sort_order: Optional[SortOrder] = None
    ):
        sort = sort or self.default_sort_key
        sort_order = sort_order or self.default_sort_order
        self._validate_sort_key(sort)

        async with self.conn as c:
            items_sorted: list[self.model] = await c.adapter.find_all(
                sort=sort, sort_order=sort_order
            )

            return items_sorted

    async def get_paginated(
        self,
        per_page: str,
        page: int,
        sort: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> PaginationResponseModel:
        sort = sort or self.default_sort_key
        sort_order = sort_order or self.default_sort_order
        self._validate_sort_key(sort)

        async with self.conn as c:
            items_paginated: PaginationResponseModel = (
                await c.adapter.find_all_with_pagination(
                    sort=sort,
                    sort_order=sort_order,
                    per_page=per_page,
                    page=page,
                )
            )

            return items_paginated
