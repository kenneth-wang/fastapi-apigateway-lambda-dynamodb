from typing import List

from pydantic import BaseModel


class CreateItemRequest(BaseModel):
    name: str
    category: str
    price: float


class ItemId(BaseModel):
    id: int


class Item(ItemId, CreateItemRequest):
    created_dt: str
    last_updated_dt: str


class ItemByDateRange(ItemId, CreateItemRequest):
    pass


class GetItemsByDateRange(BaseModel):
    items: List[ItemByDateRange]
    total_price: float


class CategoryStats(BaseModel):
    category: str
    total_price: float
    count: int


class GetCategoryStats(BaseModel):
    items: List[CategoryStats]
