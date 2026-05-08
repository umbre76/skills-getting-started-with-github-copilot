"""Tests for GET /activities endpoint using AAA pattern"""


def test_get_all_activities_returns_200(client):
    """
    Arrange: TestClient is ready
    Act: Make GET request to /activities
    Assert: Response status is 200
    """
    # Arrange
    expected_status = 200

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == expected_status


def test_get_all_activities_returns_dict_structure(client):
    """
    Arrange: TestClient is ready
    Act: Make GET request to /activities
    Assert: Response contains activities as a dictionary
    """
    # Arrange
    # (nothing to arrange, just testing the response structure)

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_all_activities_contains_required_fields(client):
    """
    Arrange: TestClient is ready
    Act: Make GET request to /activities
    Assert: Each activity has required fields (description, schedule, max_participants, participants)
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_details, dict), f"{activity_name} should be a dictionary"
        assert required_fields.issubset(
            activity_details.keys()
        ), f"{activity_name} missing required fields"
        assert isinstance(
            activity_details["participants"], list
        ), f"{activity_name} participants should be a list"


def test_get_all_activities_participants_are_strings(client):
    """
    Arrange: TestClient is ready
    Act: Make GET request to /activities
    Assert: Each participant in the list is a string (email)
    """
    # Arrange
    # (nothing to arrange)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_details in activities.items():
        for participant in activity_details["participants"]:
            assert isinstance(
                participant, str
            ), f"Participant in {activity_name} should be a string"
