import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    # Use a unique email to avoid duplicate error
    response = client.post("/activities/Chess%20Club/signup?email=tester1@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester1@mergington.edu for Chess Club" in response.json()["message"]


def test_signup_for_activity_duplicate():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=tester2@mergington.edu")
    # Duplicate signup
    response = client.post("/activities/Programming%20Class/signup?email=tester2@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=tester3@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
