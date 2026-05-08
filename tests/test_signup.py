"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_successful_with_valid_activity_and_email(client):
    """
    Arrange: Prepare valid activity name and email
    Act: Make POST request to signup endpoint
    Assert: Response status is 200 and contains success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    expected_status = 200

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == expected_status
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_nonexistent_activity_returns_404(client):
    """
    Arrange: Prepare non-existent activity name and valid email
    Act: Make POST request to signup endpoint with invalid activity
    Assert: Response status is 404
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    expected_status = 404

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == expected_status
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email_returns_400(client):
    """
    Arrange: Find an activity with existing participant, prepare to signup with same email
    Act: Make POST request to signup endpoint with already-signed-up email
    Assert: Response status is 400 (already signed up)
    """
    # Arrange
    activity_name = "Chess Club"
    # Get the activity to find an existing participant
    activities_response = client.get("/activities")
    existing_email = activities_response.json()[activity_name]["participants"][0]
    expected_status = 400

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_email}"
    )

    # Assert
    assert response.status_code == expected_status
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_adds_participant_to_activity(client):
    """
    Arrange: Prepare valid activity and new email, get initial participant count
    Act: Make signup request, then fetch activities again
    Assert: New participant appears in the activity's participant list
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = "newprogrammer@mergington.edu"
    
    # Get initial activities
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )

    # Assert
    assert signup_response.status_code == 200
    
    # Verify participant was added
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    assert new_email in updated_participants
    assert len(updated_participants) == initial_count + 1


def test_signup_response_contains_message_field(client):
    """
    Arrange: Prepare valid activity and email
    Act: Make POST request to signup endpoint
    Assert: Response JSON contains 'message' field with expected text
    """
    # Arrange
    activity_name = "Art Club"
    email = "artist@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    data = response.json()

    # Assert
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
