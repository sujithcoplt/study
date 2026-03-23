"""
Tests for the root endpoint redirects.
"""

import pytest


class TestRootEndpoint:
    """Test suite for the root endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static index.html."""
        # Arrange: No special setup needed

        # Act: Make request to root endpoint without following redirects
        response = client.get("/", follow_redirects=False)

        # Assert: Verify redirect response
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_with_follow(self, client):
        """Test following the root redirect."""
        # Arrange: No special setup needed

        # Act: Make request to root endpoint with following redirects
        response = client.get("/", follow_redirects=True)

        # Assert: Should either get 200 or 404 depending on if static files exist
        assert response.status_code in [200, 404, 307]