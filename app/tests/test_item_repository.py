from app.models.items import Item
from app.repositories.items import ItemRepository


item_repository = ItemRepository()


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


def test_get_all_items():
    # "all" category
    items = item_repository.get_items_by_category("all")

    for item in items:
        assert isinstance(item, Item)

    # specific category
    # TODO
