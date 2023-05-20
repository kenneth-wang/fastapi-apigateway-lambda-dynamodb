from fastapi.testclient import TestClient
from app.main import app
from app.models.items import CreateItemRequest


client = TestClient(app)


def test_create_item(setup_test_data):
    item = CreateItemRequest(name="Notebook", category="Stationary", price=5.5)
    response = client.post("/items", json=item.dict())
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_items(setup_test_data):
    dt_from = "2022-01-01 10:00:00"
    dt_to = "2022-01-25 10:00:00"
    response = client.get(f"/items?dt_from={dt_from}&dt_to={dt_to}")
    data = response.json()
    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Item 1"
    assert data["total_price"] == 5.5


def test_get_items_by_category(setup_test_data):
    # all categories
    response = client.get("/items/statistics?category=all")
    data = response.json()
    assert response.status_code == 200
    assert len(data["items"]) == 2
    assert data["items"][0] == {
        "category": "Stationary",
        "total_price": 5.5,
        "count": 1
    }
    assert data["items"][1] == {
        "category": "Gift",
        "total_price": 20,
        "count": 2
    }

    # single category
    response = client.get("/items/statistics?category=Gift")
    data = response.json()
    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0] == {
        "category": "Gift",
        "total_price": 20,
        "count": 2
    }
