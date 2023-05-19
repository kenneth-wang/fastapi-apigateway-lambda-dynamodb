from unittest.mock import MagicMock
from app.models.items import CreateItemRequest
from app.services.items import ItemService



def test_create_item():
    repository_mock = MagicMock()
    service = ItemService(repository_mock)
    req = CreateItemRequest(name="Notebook", category="Stationary", price=5.5)
    service.create_item(req)
    repository_mock.create_item.assert_called_once()


def test_get_items_by_date_range():
    repository_mock = MagicMock()
    service = ItemService(repository_mock)
    dt_from = "2022-01-01 10:00:00"
    dt_to = "2022-01-25 10:00:00"
    service.get_items_by_date_range(dt_from, dt_to)
    repository_mock.get_items_by_date_range.assert_called_with(dt_from, dt_to)


def test_get_items_by_category():
    repository_mock = MagicMock()
    service = ItemService(repository_mock)
    category = "all"
    service.get_items_by_category(category)
    repository_mock.get_items_by_category.assert_called_with(category)