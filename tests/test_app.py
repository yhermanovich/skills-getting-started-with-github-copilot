import pytest
from fastapi.testclient import TestClient

# Arrange-Act-Assert pattern is used in all tests

def test_root_redirects_to_static_index(client):
    # Arrange: (client fixture provided)
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307
    assert "text/html" in response.headers.get("content-type", "")
    assert "Mergington High School" in response.text

def test_get_activities_returns_all(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())

def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "test1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")
    # Confirm participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "test2@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")

def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "test3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
