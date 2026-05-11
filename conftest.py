import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Returns a basic APIClient instance."""
    return APIClient()

@pytest.fixture
def user():
    """Returns a newly created user via UserFactory."""
    from accounts.tests.factories import UserFactory
    return UserFactory()

@pytest.fixture
def authenticated_client(api_client, user):
    """Returns an APIClient authenticated with the user fixture."""
    api_client.force_authenticate(user=user)
    return api_client
