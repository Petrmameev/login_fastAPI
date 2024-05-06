from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_access_token():

    login_data = {"username": "petr", "password": "mameev"}

    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_access_token_fail():
    login_data = {"username": "petr", "password": "udushvidvjdsl"}
    response = client.post("/token", data=login_data)
    assert response.status_code == 401


def test_read_salary_without_token():
    response = client.get("/salary")
    assert response.status_code == 401


def test_read_salary_with_token():
    login_data = {"username": "petr", "password": "mameev"}
    login_response = client.post("/token", data=login_data)
    access_token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/salary", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()
    assert "salary" in response.json()
    assert "next_raise" in response.json()
