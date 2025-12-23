import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    # Sign up a new participant
    activity = "Basketball Team"
    email = "testuser@example.com"
    signup_url = f"/activities/{activity}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Unregister the participant
    unregister_url = f"/unregister/{activity}/{email}"
    response = client.delete(unregister_url)
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Unregister again should 404
    response = client.delete(unregister_url)
    assert response.status_code == 404

    # Sign up again, then try duplicate signup
    response = client.post(signup_url)
    assert response.status_code == 200
    response = client.post(signup_url)
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
