import pytest


def test_root_redirect(client):
    """Test that root redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client, reset_activities):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) >= 2


def test_signup_success(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]


def test_signup_duplicate(client, reset_activities):
    """Test that duplicate signup is rejected"""
    client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client, reset_activities):
    """Test signup for non-existent activity"""
    response = client.post("/activities/Fake%20Club/signup?email=student@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_success(client, reset_activities):
    """Test successful participant removal"""
    client.post("/activities/Chess%20Club/signup?email=removetest@mergington.edu")
    response = client.delete(
        "/activities/Chess%20Club/participants?email=removetest@mergington.edu"
    )
    assert response.status_code == 200
    assert "Removed removetest@mergington.edu from Chess Club" in response.json()["message"]


def test_remove_participant_not_found(client, reset_activities):
    """Test removing non-existent participant"""
    response = client.delete(
        "/activities/Chess%20Club/participants?email=notregistered@mergington.edu"
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_from_nonexistent_activity(client, reset_activities):
    """Test removing from non-existent activity"""
    response = client.delete(
        "/activities/Fake%20Club/participants?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
