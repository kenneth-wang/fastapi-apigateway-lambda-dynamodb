import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.items import CreateItemRequest
from app.repositories.items import ItemRepository
from app.models.items import Item


client = TestClient(app)


@pytest.fixture(scope="module")
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
        price=7.5,
        created_dt="2022-01-01 10:00:00",
        last_updated_dt="2022-01-01 10:00:00",
    )
    item_repository.create_item(item2)


def test_create_item(setup_test_data):
    item = CreateItemRequest(name="Notebook", category="Stationary", price=5.5)
    response = client.post("/items", json=item.dict())
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_items(setup_test_data):
    dt_from = "2022-01-01 10:00:00"
    dt_to = "2022-01-25 10:00:00"
    response = client.get(f"/items?dt_from={dt_from}&dt_to={dt_to}")
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total_price" in response.json()


def test_get_items_by_category():
    response = client.get("/items/statistics?category=all")
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total_price" in response.json()
