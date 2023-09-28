from typing import Any

from pydantic import BaseModel


class PaginationRequestModel(BaseModel):
    page: int
    per_page: int
    total_items: int
    total_pages: int


class PaginationResponseModel(PaginationRequestModel):
    data: list[Any]
