from collections import defaultdict
from datetime import datetime
from typing import Any, Dict
from app.models.items import GetCategoryStats, Item, GetItemsByDateRange, ItemId
from app.models.items import CreateItemRequest
from app.repositories.items import ItemRepository
import uuid

from app.utils.constants import DATETIME_STR_FORMAT


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def insert_or_update_item(self, req: CreateItemRequest) -> ItemId:
        # Given business logic: If re-insert an item with the same name,
        # the record should be updated with the new price

        matched_items = self.repository.get_items_by_name(req.name)

        if matched_items:
            assert len(matched_items) == 1
            existing_item = matched_items[0]
            self.repository.update_item(existing_item.id, existing_item.price)
            return ItemId(id=existing_item.id)

        now = datetime.now().strftime(DATETIME_STR_FORMAT)
        item = Item(
            **{
                "id": uuid.uuid4(),
                "created_dt": now,
                "last_updated_dt": now,
                **req.dict(),
            }
        )
        inserted_item = self.repository.create_item(item)
        return ItemId(id=inserted_item.id)


    def get_items_by_date_range(self, dt_from: str, dt_to: str) -> GetItemsByDateRange:
        items = self.repository.get_items_by_date_range(dt_from, dt_to)
        total_price = sum(item.price for item in items)

        return GetItemsByDateRange(**{"items": items, "total_price": total_price})

    def get_items_by_category(self, category: str) -> GetCategoryStats:
        items = self.repository.get_items_by_category(category)

        categories: Dict[str, Any] = defaultdict(
            lambda: {"category": "", "count": 0, "total_price": 0.0}
        )

        for item in items:
            categories[item.category]["category"] = item.category
            categories[item.category]["count"] += 1
            categories[item.category]["total_price"] += item.price

        return GetCategoryStats(**{"items": list(categories.values())})
