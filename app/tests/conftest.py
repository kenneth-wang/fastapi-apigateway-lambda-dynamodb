import pytest
from app.models.items import Item

from app.repositories.items import ItemRepository

@pytest.fixture()
def item_repository():
    repository = ItemRepository()
    yield repository
    repository.delete_all_items()


@pytest.fixture
def setup_test_data(item_repository):
    item1 = Item(
        id=1,
        name="Item 1",
        category="Stationary",
        price=5.5,
        created_dt="2022-01-01 10:00:00",
        last_updated_dt="2022-01-01 10:00:00",
    )
    item_repository.create_item(item1)

    item2 = Item(
        id=2,
        name="Item 2",
        category="Gift",
        price=18,
        created_dt="2022-01-01 10:00:00",
        last_updated_dt="2022-01-30 10:00:00",
    )
    item_repository.create_item(item2)

    item3 = Item(
        id=3,
        name="Item 3",
        category="Gift",
        price=2,
        created_dt="2022-01-01 10:00:00",
        last_updated_dt="2022-01-30 10:00:00",
    )
    item_repository.create_item(item3)
