import requests
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8001/api/v1"


def post(base_url, path, json=None):
    return requests.post(f"{base_url}{path}", json=json)


def get(base_url, path):
    return requests.get(f"{base_url}{path}")


def delete(base_url, path):
    return requests.delete(f"{base_url}{path}")
