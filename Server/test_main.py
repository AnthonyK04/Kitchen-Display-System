import pytest
from pathlib import Path
from fastapi.testclient import TestClient
import db
from main import app, get_db_path

TEST_DB = "test_items.db"

def override_get_db_path():
    return TEST_DB

app.dependency_overrides[get_db_path] = override_get_db_path

@pytest.fixture(autouse=True)
def setup_and_teardown():
    db.init_db(db_path=TEST_DB)
    yield
    Path(TEST_DB).unlink(missing_ok=True)

client = TestClient(app)


def test_add_menu_item():
    response = client.post("/menu-items", json={"name": "Fries"})
    assert response.status_code == 200

    response = client.get("/menu-items")
    menu_items = response.json()
    assert len(menu_items) == 1
    assert menu_items[0]["name"] == "fries"

def test_pending_to_done_workflow():
    response = client.post("/items",json={"name":"Orange Chicken","qty":3})
    assert response.status_code == 200

    response = client.get("/items/pending")
    assert response.json()[0]["id"] == 1
    item_id = response.json()[0]["id"]
    response = client.patch(f"/items/{item_id}/done")
    assert response.status_code == 200

    response = client.get("/items/pending")
    assert len(response.json()) == 0

    response = client.get("/items")
    assert response.json()[0]["status"] == "done"

def test_delete_item():
    response = client.post("/items", json={"name": "Fries", "qty": 2})
    assert response.status_code == 200

    response = client.get("/items/pending")
    pending_items = response.json()
    assert len(pending_items) == 1
    item_id = pending_items[0]["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200

    response = client.get("/items")
    all_items = response.json()
    matching = [item for item in all_items if item["id"] == item_id]
    assert len(matching) == 0


def test_delete_menu_item():
    response = client.post("/menu-items", json={"name": "Egg Roll"})
    assert response.status_code == 200

    response = client.get("/menu-items")
    menu_items = response.json()
    assert len(menu_items) == 1
    item_id = menu_items[0]["id"]

    response = client.delete(f"/menu-items/{item_id}")
    assert response.status_code == 200

    response = client.get("/menu-items")
    assert len(response.json()) == 0


def test_add_item_missing_qty_fails():
    response = client.post("/items", json={"name": "Fries"})
    assert response.status_code == 422


def test_add_item_wrong_type_fails():
    response = client.post("/items", json={"name": "Fries", "qty": "two"})
    assert response.status_code == 422


def test_mark_nonexistent_item_done():
    response = client.patch("/items/9999/done")
    assert response.status_code == 200
