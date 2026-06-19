import urllib.parse


def test_get_activities(client, app_module_fixture):
    # Arrange: nothing to set up, using initial in-memory activities
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    assert resp.json() == app_module_fixture.activities


def test_signup_success(client, app_module_fixture):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@example.com"
    url = f"/activities/{urllib.parse.quote(activity, safe='')}/signup"
    assert email not in app_module_fixture.activities[activity]["participants"]

    # Act
    resp = client.post(url, params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app_module_fixture.activities[activity]["participants"]


def test_signup_duplicate(client, app_module_fixture):
    # Arrange
    activity = "Chess Club"
    existing = app_module_fixture.activities[activity]["participants"][0]
    url = f"/activities/{urllib.parse.quote(activity, safe='')}/signup"

    # Act
    resp = client.post(url, params={"email": existing})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity(client):
    # Arrange
    activity = "Nonexistent Activity"
    url = f"/activities/{urllib.parse.quote(activity, safe='')}/signup"

    # Act
    resp = client.post(url, params={"email": "someone@example.com"})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_delete_participant_success(client, app_module_fixture):
    # Arrange
    activity = "Basketball Team"
    email = app_module_fixture.activities[activity]["participants"][0]
    url = (
        f"/activities/{urllib.parse.quote(activity, safe='')}/participants/"
        f"{urllib.parse.quote(email, safe='')}"
    )

    # Act
    resp = client.delete(url)

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in app_module_fixture.activities[activity]["participants"]


def test_delete_participant_missing(client, app_module_fixture):
    # Arrange
    activity = "Basketball Team"
    missing_email = "missing@example.com"
    url = (
        f"/activities/{urllib.parse.quote(activity, safe='')}/participants/"
        f"{urllib.parse.quote(missing_email, safe='')}"
    )

    # Act
    resp = client.delete(url)

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in activity"
