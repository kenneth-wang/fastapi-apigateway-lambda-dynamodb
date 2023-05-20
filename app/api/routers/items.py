from fastapi import APIRouter

from app.models.items import (
    CreateItemRequest,
    GetCategoryStats,
    GetItemsByDateRange,
    ItemId,
)
from app.repositories.items import ItemRepository
from app.services.items import ItemService

router = APIRouter()
repository = ItemRepository()
service = ItemService(repository)


@router.post("", status_code=201)
def create_item(req: CreateItemRequest) -> ItemId:
    return service.insert_or_update_item(req)


@router.get("")
def get_items(dt_from: str, dt_to: str) -> GetItemsByDateRange:
    return service.get_items_by_date_range(dt_from, dt_to)


@router.get("/statistics")
def get_items_by_category(category: str) -> GetCategoryStats:
    return service.get_items_by_category(category)
