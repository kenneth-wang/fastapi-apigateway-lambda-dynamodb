import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from typing import List
from app.models.items import Item


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
    last_updated_at = UnicodeAttribute()



if not ItemTable.exists():
    ItemTable.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


class ItemRepository:
    def __init__(self):
        self.table = ItemTable

    def create_item(self, item: Item) -> Item:
        item_table = ItemTable(id=item.id, name=item.name, category=item.category,
                               price=item.price, created_dt=item.created_dt,
                               last_updated_at=item.last_updated_at)
        item_table.save()
        return item

    def get_items_by_date_range(self, dt_from: str, dt_to: str) -> List[Item]:
        items = ItemTable.scan((ItemTable.last_updated_at >= dt_from) &
                               (ItemTable.last_updated_at <= dt_to))
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
            last_updated_at=item_table.last_updated_at
        )

    @staticmethod
    def delete_all_items():
        items = ItemTable.scan()
        for item in items:
            item.delete()