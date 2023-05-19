from datetime import datetime
from typing import List
from app.models.items import Item
from app.models.items import CreateItemRequest
from app.repositories.items import ItemRepository
import uuid

from app.utils.constants import DATETIME_STR_FORMAT


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create_item(self, req: CreateItemRequest):
        # TODO:
        # Given business logic: If re-insert an item with the same name,
        # the record should be updated with the new price

        # Add response schema

        now = datetime.now().strftime(DATETIME_STR_FORMAT)
        item = Item(
            **{
                "id": uuid.uuid4(),
                "created_dt": now,
                "last_updated_dt": now,
                **req.dict(),
            }
        )
        return self.repository.create_item(item)

    def get_items_by_date_range(self, dt_from: str, dt_to: str) -> List[Item]:
        # TODO: Fix schema. Add response schema
        return self.repository.get_items_by_date_range(dt_from, dt_to)

    def get_items_by_category(self, category: str) -> List[Item]:
        # TODO: Fix schema. Add response schema
        return self.repository.get_items_by_category(category)
