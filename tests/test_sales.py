import requests
import pytest

from conftest import post, get, delete


USER_PAYLOAD = {
    "user_name": "sale test",
    "user_age": 30,
    "bought_premium": False,
}

THING_PAYLOAD = {
    "category": "food",
    "price": 150,
}


@pytest.fixture(scope="function")
def sale_deps(base_url):
    user = post(base_url, "/users", json=USER_PAYLOAD).json()
    thing = post(base_url, "/things", json=THING_PAYLOAD).json()
    yield user["user_id"], thing["thing_id"]
    delete(base_url, f"/users/{user['user_id']}")
    delete(base_url, f"/things/{thing['thing_id']}")


@pytest.fixture(scope="function")
def created_sale_id(base_url, sale_deps):
    user_id, thing_id = sale_deps
    payload = {
        "user_id": user_id,
        "thing_id": thing_id,
        "count": 3,
        "payment_type": "card",
    }
    resp = post(base_url, "/sales", json=payload)
    assert resp.status_code == 200, resp.text
    sale = resp.json()
    yield sale["sale_id"]
    delete(base_url, f"/sales/{sale['sale_id']}")


def test_post_sale(base_url, sale_deps):
    user_id, thing_id = sale_deps
    payload = {
        "user_id": user_id,
        "thing_id": thing_id,
        "count": 2,
        "payment_type": "nalik",
    }
    resp = post(base_url, "/sales", json=payload)
    assert resp.status_code == 200, resp.text
    sale = resp.json()
    assert sale["user_id"] == user_id
    assert sale["thing_id"] == thing_id
    assert sale["count"] == 2
    assert sale["payment_type"] == "nalik"
    delete(base_url, f"/sales/{sale['sale_id']}")


def test_get_sales(base_url):
    resp = get(base_url, "/sales")
    assert resp.status_code == 200, resp.text
    sales = resp.json()
    assert isinstance(sales, list)
    for sale in sales:
        assert "sale_id" in sale
        assert "user_id" in sale
        assert "thing_id" in sale


def test_get_sale_by_id(base_url, created_sale_id):
    resp = get(base_url, f"/sales/{created_sale_id}")
    assert resp.status_code == 200, resp.text
    sale = resp.json()
    assert sale["sale_id"] == created_sale_id


def test_get_sale_by_missing_id(base_url):
    resp = get(base_url, "/sales/999999999")
    assert resp.status_code == 200, resp.text
    assert "error" in resp.json()


def test_delete_sale(base_url, sale_deps):
    user_id, thing_id = sale_deps
    payload = {
        "user_id": user_id,
        "thing_id": thing_id,
        "count": 5,
        "payment_type": "card",
    }
    resp = post(base_url, "/sales", json=payload)
    assert resp.status_code == 200, resp.text
    sale_id = resp.json()["sale_id"]

    resp = delete(base_url, f"/sales/{sale_id}")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"log": "deleted 1 rows" }
    
    resp = get(base_url, f"/sales/{sale_id}")
    assert "error" in resp.json()
