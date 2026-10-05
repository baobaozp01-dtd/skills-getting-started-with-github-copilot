from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_participant_from_activity():
    email = "student@example.edu"
    activity_name = "Chess Club"

    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_not_found():
    response = client.delete(
        "/activities/Chess%20Club/participants/missing@example.edu"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Participant not found in activity"
    }
