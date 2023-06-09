import os
from datetime import datetime
from typing import List

from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from app.models.items import Item
from app.utils.constants import DATETIME_STR_FORMAT


class ItemTable(Model):
    class Meta:
        table_name = "items_table"
        region = os.getenv("AWS_REGION")
        host = os.getenv("DYNAMODB_ENDPOINT")

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    category = UnicodeAttribute()
    price = NumberAttribute()
    created_dt = UnicodeAttribute()
    last_updated_dt = UnicodeAttribute()


if not ItemTable.exists():
    ItemTable.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


class ItemRepository:
    def __init__(self):
        self.table = ItemTable

    def get_item(self, id: int) -> Item:
        item = ItemTable.get(hash_key=id)

        return Item(
            id=int(item.id),
            name=item.name,
            category=item.category,
            price=item.price,
            created_dt=item.created_dt,
            last_updated_dt=item.last_updated_dt,
        )

    def update_item(self, id: int, price: float):
        item = ItemTable.get(hash_key=id)
        item.price = price
        item.last_updated_dt = datetime.now().strftime(DATETIME_STR_FORMAT)
        item.save()

    def create_item(self, item: Item) -> Item:
        item_table = ItemTable(
            id=item.id,
            name=item.name,
            category=item.category,
            price=item.price,
            created_dt=item.created_dt,
            last_updated_dt=item.last_updated_dt,
        )
        item_table.save()
        return item

    def get_items_by_name(self, name: str) -> List[Item]:
        items = ItemTable.scan(ItemTable.name == name)
        return [self._convert_item_table_to_item(item_table) for item_table in items]

    def get_items_by_date_range(self, dt_from: str, dt_to: str) -> List[Item]:
        items = ItemTable.scan(
            (ItemTable.last_updated_dt >= dt_from)
            & (ItemTable.last_updated_dt <= dt_to)
        )
        return [self._convert_item_table_to_item(item_table) for item_table in items]

    def get_items_by_category(self, category: str) -> List[Item]:
        if category == "all":
            items = ItemTable.scan()
        else:
            items = ItemTable.scan(ItemTable.category == category)
        return [self._convert_item_table_to_item(item_table) for item_table in items]

    @staticmethod
    def _convert_item_table_to_item(item_table: ItemTable) -> Item:
        return Item(
            id=int(item_table.id),
            name=item_table.name,
            category=item_table.category,
            price=item_table.price,
            created_dt=item_table.created_dt,
            last_updated_dt=item_table.last_updated_dt,
        )

    @staticmethod
    def delete_all_items():
        items = ItemTable.scan()
        for item in items:
            item.delete()
