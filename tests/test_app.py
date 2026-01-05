from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "tester@example.com"

    # Ensure not present initially (if present, try to remove first)
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    activities = resp.json()
    if email in activities.get(activity, {}).get("participants", []):
        client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Confirm participant present
    resp = client.get("/activities")
    activities = resp.json()
    assert email in activities.get(activity, {}).get("participants", [])

    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Confirm participant removed
    resp = client.get("/activities")
    activities = resp.json()
    assert email not in activities.get(activity, {}).get("participants", [])
