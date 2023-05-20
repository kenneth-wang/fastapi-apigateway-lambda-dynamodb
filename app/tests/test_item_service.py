from unittest.mock import MagicMock
from app.models.items import CreateItemRequest, Item
from app.services.items import ItemService


def test_insert_or_update_item_case_insert():
    repository_mock = MagicMock()
    service = ItemService(repository_mock)

    req = CreateItemRequest(name="Notebook", category="Stationary", price=5.5)

    repository_mock.get_items_by_name.return_value = []
    service.insert_or_update_item(req)
    repository_mock.create_item.assert_called_once()
    repository_mock.get_items_by_name.assert_called_once()


def test_insert_or_update_item_case_update():
    # test update as item with same name already exists
    repository_mock = MagicMock()
    service = ItemService(repository_mock)

    req = CreateItemRequest(name="Notebook", category="Stationary", price=5.5)

    repository_mock.get_items_by_name.return_value = [
        Item(
            id=1,
            name="Item 1",
            category="Stationary",
            price=5.5,
            created_dt="2022-01-01 10:00:00",
            last_updated_dt="2022-01-01 10:00:00",
        )
    ]
    service.insert_or_update_item(req)
    repository_mock.update_item.assert_called_once()
    repository_mock.get_items_by_name.assert_called_once()


def test_get_items_by_date_range():
    dt_from = "2022-01-01 10:00:00"
    dt_to = "2022-01-25 10:00:00"

    items = [
        Item(
            id=1,
            name="Item 1",
            category="Stationary",
            price=5.5,
            created_dt="2022-01-01 10:00:00",
            last_updated_dt="2022-01-01 10:00:00",
        )
    ]

    repository_mock = MagicMock()
    service = ItemService(repository_mock)
    repository_mock.get_items_by_date_range.return_value = items

    result = service.get_items_by_date_range(dt_from, dt_to)

    assert len(result.items) == 1
    assert result.total_price == 5.5


def test_get_items_by_category():
    repository_mock = MagicMock()
    service = ItemService(repository_mock)
    category = "all"
    service.get_items_by_category(category)
    repository_mock.get_items_by_category.assert_called_with(category)
