from fastapi import APIRouter

from app.models.items import CreateItemRequest
from app.repositories.items import ItemRepository
from app.services.items import ItemService

router = APIRouter()
repository = ItemRepository()
service = ItemService(repository)


@router.post("", status_code=201)
def create_item(req: CreateItemRequest):
    item = service.create_item(req)

    # TODO: Add response schema

    return {"id": item.id}


@router.get("")
def get_items(dt_from: str, dt_to: str):
    items = service.get_items_by_date_range(dt_from, dt_to)

    # TODO: Move logic to service file
    total_price = sum(item.price for item in items)

    # TODO: Add response schema

    response = {"items": items, "total_price": total_price}
    return response


@router.get("/statistics")
def get_items_by_category(category: str):
    items = service.get_items_by_category(category)

    # TODO: Move logic to service file
    total_price = sum(item.price for item in items)

    # TODO: Add response schema

    response = {"items": items, "total_price": total_price}
    return response
