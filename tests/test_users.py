import requests
import pytest

from conftest import post, get, delete


USER_PAYLOAD = {
    "user_name": "test user",
    "user_age": 25,
    "bought_premium": True,
}


@pytest.fixture(scope="function")
def created_user_id(base_url):
    resp = post(base_url, "/users", json=USER_PAYLOAD)
    assert resp.status_code == 200, resp.text
    user = resp.json()
    yield user["user_id"]
    delete(base_url, f"/users/{user['user_id']}")


def test_post_user(base_url):
    resp = post(base_url, "/users", json=USER_PAYLOAD)
    assert resp.status_code == 200, resp.text
    user = resp.json()
    assert user["user_name"] == USER_PAYLOAD["user_name"]
    assert user["user_age"] == USER_PAYLOAD["user_age"]
    assert user["bought_premium"] == USER_PAYLOAD["bought_premium"]
    delete(base_url, f"/users/{user['user_id']}")


def test_get_users(base_url):
    resp = get(base_url, "/users")
    assert resp.status_code == 200, resp.text
    users = resp.json()
    assert isinstance(users, list)
    for user in users:
        assert "user_id" in user
        assert "user_name" in user


def test_get_user_by_id(base_url, created_user_id):
    resp = get(base_url, f"/users/{created_user_id}")
    assert resp.status_code == 200, resp.text
    user = resp.json()
    assert user["user_id"] == created_user_id


def test_get_user_by_missing_id(base_url):
    resp = get(base_url, "/users/999999999")
    assert resp.status_code == 200, resp.text
    assert "error" in resp.json()


def test_delete_user(base_url):
    resp = post(base_url, "/users", json=USER_PAYLOAD)
    assert resp.status_code == 200, resp.text
    user_id = resp.json()["user_id"]

    resp = delete(base_url, f"/users/{user_id}")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"log": "deleted 1 rows" }

    resp = get(base_url, f"/users/{user_id}")
    assert "error" in resp.json()
    
