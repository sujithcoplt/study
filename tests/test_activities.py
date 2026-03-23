"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_all_activities_success(self, client, reset_activities):
        """Test successfully retrieving all activities."""
        # Arrange: No special setup needed, using reset_activities fixture

        # Act: Make request to get all activities
        response = client.get("/activities")

        # Assert: Verify response structure and content
        assert response.status_code == 200
        data = response.json()

        # Verify response is a dictionary
        assert isinstance(data, dict)

        # Verify all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Team", "Tennis Club", "Art Studio",
            "Music Ensemble", "Debate Club", "Science Club"
        ]
        for activity in expected_activities:
            assert activity in data

    def test_activity_structure(self, client, reset_activities):
        """Test that each activity has the correct structure."""
        # Arrange: No special setup needed

        # Act: Get activities
        response = client.get("/activities")
        data = response.json()

        # Assert: Verify structure for each activity
        required_fields = {"description", "schedule", "max_participants", "participants"}

        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
            assert required_fields.issubset(activity_data.keys()), \
                f"{activity_name} missing required fields"

            # Verify field types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_activity_participants_are_strings(self, client, reset_activities):
        """Test that all participants are email strings."""
        # Arrange: No special setup needed

        # Act: Get activities
        response = client.get("/activities")
        data = response.json()

        # Assert: Verify participants are valid email strings
        for activity_name, activity_data in data.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant, f"Participant should be valid email: {participant}"

    def test_get_activities_response_headers(self, client, reset_activities):
        """Test that response has correct content type."""
        # Arrange: No special setup needed

        # Act: Get activities
        response = client.get("/activities")

        # Assert: Verify response headers
        assert response.headers["content-type"] == "application/json"