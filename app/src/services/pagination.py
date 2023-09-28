from fastapi import HTTPException
from pydantic import BaseModel

from core.constants import SortOrder
from core.messages import INVALID_SORT_PARAM
from db.db import DBConnector
from models.pagination import PaginationResponseModel


class PaginationService:
    def __init__(
        self,
        model: BaseModel,
        connection: DBConnector,
        default_sort_key: str | None = None,
        exclude_sort_keys: list[str] | None = None,
    ):
        self.conn = connection
        self.default_sort_key = default_sort_key
        self.avaliable_sort_keys = self._get_keys_for_sort(model, exclude_sort_keys)

    def _get_keys_for_sort(self, model: BaseModel, exclude_sort_keys: list[str] | None):
        keys = [field_name for field_name in model.model_fields.keys()]

        if exclude_sort_keys:
            return [key for key in keys if key not in exclude_sort_keys]

        return keys

    def _validate_sort_key(self, sort: str):
        if sort not in self.avaliable_sort_keys:
            sort_keys_str = " ".join(self.avaliable_sort_keys)
            raise HTTPException(400, INVALID_SORT_PARAM.format(sort, sort_keys_str))

    async def get_sorted(self, sort: str, sort_order: SortOrder):
        self._validate_sort_key(sort)
        async with self.conn as c:
            items_sorted: list[self.model] = await c.adapter.find_all_with_sort(
                sort, sort_order
            )

            return items_sorted

    async def get_paginated(
        self, sort: str, sort_order: str, per_page: str, page: int
    ) -> PaginationResponseModel:
        self._validate_sort_key(sort)
        async with self.conn as c:
            items_paginated: PaginationResponseModel = (
                await c.adapter.find_all_with_pagination(
                    sort,
                    sort_order,
                    per_page,
                    page,
                )
            )

            return items_paginated
