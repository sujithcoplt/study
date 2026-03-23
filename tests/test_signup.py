"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""

    def test_signup_new_student_success(self, client, reset_activities):
        """Test successfully signing up a new student."""
        # Arrange: Prepare test data
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act: Make signup request
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Verify successful response
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

        # Verify student was added to activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]

    def test_signup_duplicate_student_fails(self, client, reset_activities):
        """Test that signing up a student twice fails."""
        # Arrange: Sign up once first
        email = "duplicate@mergington.edu"
        activity = "Chess Club"

        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Act: Try to sign up again
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Second signup should fail
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_already_participant_fails(self, client, reset_activities):
        """Test that signing up an already enrolled student fails."""
        # Arrange: Use an email that's already in the activity
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act: Try to sign up existing participant
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Should fail
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        """Test signup fails for non-existent activity."""
        # Arrange: Use non-existent activity name
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"

        # Act: Try to sign up for non-existent activity
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Should fail with 404
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_signup_multiple_students(self, client, reset_activities):
        """Test signing up multiple different students."""
        # Arrange: Prepare multiple emails
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        activity = "Art Studio"

        # Act: Sign up all students
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert: Verify all students were added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        for email in emails:
            assert email in activities_data[activity]["participants"]

    def test_signup_with_special_characters_in_email(self, client, reset_activities):
        """Test signup with valid email formats."""
        # Arrange: Use email with special characters
        email = "john.doe+tag@mergington.edu"
        activity = "Music Ensemble"

        # Act: Sign up with special email
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Should succeed
        assert response.status_code == 200

    def test_signup_case_sensitive_activity_name(self, client, reset_activities):
        """Test that activity names are case-sensitive."""
        # Arrange: Use lowercase version of existing activity
        email = "student@mergington.edu"
        activity = "chess club"  # lowercase, should not match "Chess Club"

        # Act: Try to sign up for lowercase activity
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Should fail because activity name is case-sensitive
        assert response.status_code == 404

    def test_signup_response_format(self, client, reset_activities):
        """Test the response format of successful signup."""
        # Arrange: Prepare signup data
        email = "test@mergington.edu"
        activity = "Science Club"

        # Act: Make signup request
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert: Verify response format
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)