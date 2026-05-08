"""Integration tests for end-to-end signup flows using AAA pattern"""


def test_signup_flow_signup_appears_in_activities_list(client):
    """
    Arrange: Pick an activity and a new email
    Act: 1. Get initial activities 2. Sign up student 3. Get activities again
    Assert: New participant appears in the activity's participant list
    """
    # Arrange
    activity_name = "Debate Team"
    new_email = "debater@mergington.edu"

    # Act - Step 1: Get initial activities
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    initial_count = len(initial_participants)

    # Act - Step 2: Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )

    # Act - Step 3: Get activities again
    final_response = client.get("/activities")
    final_participants = final_response.json()[activity_name]["participants"]
    final_count = len(final_participants)

    # Assert
    assert signup_response.status_code == 200
    assert new_email in final_participants
    assert final_count == initial_count + 1


def test_multiple_students_can_signup_for_different_activities(client):
    """
    Arrange: Prepare two different activities and two different emails
    Act: Sign up first student for activity 1, second student for activity 2
    Assert: Both signups succeed and both students appear in their respective activities
    """
    # Arrange
    activity1 = "Math Olympiad"
    activity2 = "Drama Workshop"
    email1 = "mathstudent@mergington.edu"
    email2 = "dramatist@mergington.edu"

    # Act - Signup 1
    response1 = client.post(
        f"/activities/{activity1}/signup?email={email1}"
    )

    # Act - Signup 2
    response2 = client.post(
        f"/activities/{activity2}/signup?email={email2}"
    )

    # Act - Verify both students in their activities
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 in activities[activity1]["participants"]
    assert email2 in activities[activity2]["participants"]
    assert email1 not in activities[activity2]["participants"]
    assert email2 not in activities[activity1]["participants"]


def test_multiple_students_can_signup_for_same_activity(client):
    """
    Arrange: Prepare one activity and two different emails
    Act: Sign up both students for the same activity
    Assert: Both signups succeed and both students appear in the activity
    """
    # Arrange
    activity_name = "Soccer Team"
    email1 = "soccer_player1@mergington.edu"
    email2 = "soccer_player2@mergington.edu"

    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act - Signup 1
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={email1}"
    )

    # Act - Signup 2
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={email2}"
    )

    # Act - Verify both in the activity
    final_response = client.get("/activities")
    final_participants = final_response.json()[activity_name]["participants"]
    final_count = len(final_participants)

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 in final_participants
    assert email2 in final_participants
    assert final_count == initial_count + 2


def test_full_user_journey_view_and_signup(client):
    """
    Arrange: User journey starting from root
    Act: 1. Access root (gets redirected to HTML) 2. Get activities via API 3. Sign up for one
    Assert: All steps succeed and participant is registered
    """
    # Arrange
    activity_name = "Gym Class"
    email = "athlete@mergington.edu"

    # Act - Step 1: Access root
    root_response = client.get("/", follow_redirects=True)

    # Act - Step 2: Get activities (as frontend would do)
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Act - Step 3: Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert root_response.status_code == 200
    assert activities_response.status_code == 200
    assert activity_name in activities
    assert signup_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"] or email in client.get("/activities").json()[activity_name]["participants"]
