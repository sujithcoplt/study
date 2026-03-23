"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest


class TestRemoveParticipant:
    """Test suite for removing participants from activities."""

    def test_remove_existing_participant_success(self, client, reset_activities):
        """Test successfully removing an existing participant."""
        # Arrange: Use existing participant
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act: Remove the participant
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert: Verify successful response
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "removed" in data["message"].lower()

        # Verify participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]

    def test_remove_nonexistent_participant_fails(self, client, reset_activities):
        """Test removing a participant who is not in the activity."""
        # Arrange: Use email not in the activity
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"

        # Act: Try to remove non-existent participant
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert: Should fail with 404
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_fails(self, client, reset_activities):
        """Test removing from an activity that doesn't exist."""
        # Arrange: Use non-existent activity
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"

        # Act: Try to remove from non-existent activity
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert: Should fail with 404
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_remove_multiple_participants(self, client, reset_activities):
        """Test removing multiple participants from same activity."""
        # Arrange: First add some students
        activity = "Tennis Club"
        emails_to_add = ["extra1@mergington.edu", "extra2@mergington.edu"]

        for email in emails_to_add:
            client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )

        # Act: Remove them
        response1 = client.delete(
            f"/activities/{activity}/participants/extra1@mergington.edu"
        )
        response2 = client.delete(
            f"/activities/{activity}/participants/extra2@mergington.edu"
        )

        # Assert: Both removals should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "extra1@mergington.edu" not in activities_data[activity]["participants"]
        assert "extra2@mergington.edu" not in activities_data[activity]["participants"]

    def test_remove_original_participant(self, client, reset_activities):
        """Test removing one of the original participants."""
        # Arrange: Use original participant
        email = "emma@mergington.edu"
        activity = "Programming Class"

        # Act: Remove original participant
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert: Should succeed
        assert response.status_code == 200

        # Verify other participants remain
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "sophia@mergington.edu" in activities_data[activity]["participants"]
        assert email not in activities_data[activity]["participants"]

    def test_remove_response_format(self, client, reset_activities):
        """Test the response format of successful removal."""
        # Arrange: Use existing participant
        email = "grace@mergington.edu"
        activity = "Debate Club"

        # Act: Remove participant
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert: Verify response format
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)

    def test_remove_case_sensitive_email(self, client, reset_activities):
        """Test that email matching is case-sensitive."""
        # Arrange: Use uppercase version of existing email
        email = "MICHAEL@MERGINGTON.EDU"  # uppercase, should not match "michael@mergington.edu"
        activity = "Chess Club"

        # Act: Try to remove with uppercase email
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert: Should fail because email is case-sensitive
        assert response.status_code == 404