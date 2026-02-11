from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data


def test_signup_duplicate_and_unsignup_flow():
    activity = "Tennis Club"
    email = "testuser@mergington.edu"

    # Sign up the user
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in res.json()["message"]

    # Duplicate signup should fail with 400
    res_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res_dup.status_code == 400

    # Unregister the user
    res_un = client.delete(f"/activities/{activity}/unsignup", params={"email": email})
    assert res_un.status_code == 200
    assert email in res_un.json()["message"]

    # Verify the user is no longer in participants
    res_final = client.get("/activities")
    assert res_final.status_code == 200
    participants = res_final.json()[activity]["participants"]
    assert email not in participants
