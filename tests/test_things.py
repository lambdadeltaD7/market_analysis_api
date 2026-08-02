import requests
import pytest

from conftest import post, get, delete


THING_PAYLOAD = {
    "category": "food",
    "price": 100,
}


@pytest.fixture(scope="function")
def created_thing_id(base_url):
    resp = post(base_url, "/things", json=THING_PAYLOAD)
    assert resp.status_code == 200, resp.text
    thing = resp.json()
    yield thing["thing_id"]
    delete(base_url, f"/things/{thing['thing_id']}")


def test_post_thing(base_url):
    resp = post(base_url, "/things", json=THING_PAYLOAD)
    assert resp.status_code == 200, resp.text
    thing = resp.json()
    assert thing["category"] == THING_PAYLOAD["category"]
    assert thing["price"] == THING_PAYLOAD["price"]
    delete(base_url, f"/things/{thing['thing_id']}")


def test_get_things(base_url):
    resp = get(base_url, "/things")
    assert resp.status_code == 200, resp.text
    things = resp.json()
    assert isinstance(things, list)
    for thing in things:
        assert "thing_id" in thing
        assert "category" in thing


def test_get_thing_by_id(base_url, created_thing_id):
    resp = get(base_url, f"/things/{created_thing_id}")
    assert resp.status_code == 200, resp.text
    thing = resp.json()
    assert thing["thing_id"] == created_thing_id


def test_get_thing_by_missing_id(base_url):
    resp = get(base_url, "/things/999999999")
    assert resp.status_code == 200, resp.text
    assert "error" in resp.json()


def test_delete_thing(base_url):
    resp = post(base_url, "/things", json=THING_PAYLOAD)
    assert resp.status_code == 200, resp.text
    thing_id = resp.json()["thing_id"]

    resp = delete(base_url, f"/things/{thing_id}")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"log": "deleted 1 rows" }
    
    resp = get(base_url, f"/things/{thing_id}")
    assert "error" in resp.json()
