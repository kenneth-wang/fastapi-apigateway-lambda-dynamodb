from datetime import datetime

from freezegun import freeze_time

from app.models.items import Item
from app.repositories.items import ItemRepository

item_repository = ItemRepository()


def test_get_item(setup_test_data):
    retrieved_item = item_repository.get_item(1)

    assert retrieved_item.id == 1
    assert retrieved_item.name == "Item 1"
    assert retrieved_item.category == "Stationary"
    assert retrieved_item.price == 5.5
    assert retrieved_item.created_dt == "2022-01-01 10:00:00"
    assert retrieved_item.last_updated_dt == "2022-01-01 10:00:00"


@freeze_time(datetime(year=2022, month=6, day=15, hour=0, minute=0, second=0))
def test_update_item(setup_test_data):
    new_price = 4.5
    item_id = 1
    item_repository.update_item(item_id, new_price)

    updated_item = item_repository.get_item(item_id)

    assert updated_item.price == new_price
    assert updated_item.last_updated_dt == "2022-06-15 00:00:00"


def test_create_item():
    item = Item(
        id=1,
        name="Notebook",
        category="Stationary",
        price=5.5,
        created_dt="2022-01-01",
        last_updated_dt="2022-01-01",
    )

    created_item = item_repository.create_item(item)

    assert created_item.id == item.id
    assert created_item.name == item.name
    assert created_item.category == item.category
    assert created_item.price == item.price
    assert created_item.created_dt == item.created_dt
    assert created_item.last_updated_dt == item.last_updated_dt


def test_get_items_by_date_range():
    items = item_repository.get_items_by_date_range("2022-01-01", "2022-01-31")

    for item in items:
        assert isinstance(item, Item)


def test_get_items_by_category():
    items = item_repository.get_items_by_category("Stationary")

    for item in items:
        assert isinstance(item, Item)
        assert item.category == "Stationary"
