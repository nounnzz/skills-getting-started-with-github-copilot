from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert activity_name in payload


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"].copy()
    email = "new.student@mergington.edu"

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"].copy()
    email = original_participants[0]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    finally:
        activities[activity_name]["participants"] = original_participants
