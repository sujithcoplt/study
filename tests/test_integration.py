"""
Integration tests for complete workflows.
"""

import pytest


class TestIntegrationWorkflows:
    """Test complete user workflows across multiple endpoints."""

    def test_workflow_signup_and_view(self, client, reset_activities):
        """Test the workflow of signing up and viewing activities."""
        # Arrange: Prepare test data
        email = "workflow@mergington.edu"
        activity = "Chess Club"

        # Get initial activity list
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity]["participants"])

        # Act: Sign up for activity
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200

        # View updated activity list
        updated_response = client.get("/activities")
        updated_data = updated_response.json()
        updated_count = len(updated_data[activity]["participants"])

        # Assert: Verify count increased
        assert updated_count == initial_count + 1
        assert email in updated_data[activity]["participants"]

    def test_workflow_signup_remove_signup(self, client, reset_activities):
        """Test signing up, removing, and signing up again."""
        # Arrange: Prepare test data
        email = "cycle@mergington.edu"
        activity = "Art Studio"

        # Act: Sign up
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Remove
        response2 = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response2.status_code == 200

        # Sign up again
        response3 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response3.status_code == 200

        # Assert: Verify final state
        final_response = client.get("/activities")
        final_data = final_response.json()
        assert email in final_data[activity]["participants"]

    def test_workflow_multiple_activities_signup(self, client, reset_activities):
        """Test signing up for multiple activities."""
        # Arrange: Prepare test data
        email = "multi@mergington.edu"
        activities_to_join = ["Chess Club", "Science Club", "Music Ensemble"]

        # Act: Sign up for multiple activities
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert: Verify student is in all activities
        final_response = client.get("/activities")
        final_data = final_response.json()

        for activity in activities_to_join:
            assert email in final_data[activity]["participants"]

    def test_workflow_error_handling(self, client, reset_activities):
        """Test error handling throughout a workflow."""
        # Arrange: Prepare test data
        email = "error@mergington.edu"
        activity = "Gym Class"

        # Act: Try to sign up twice
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 400

        # Try to remove twice
        client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 404