import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db

class TestUserRegistrationView:
    def test_successful_registration(self, api_client):
        # Arrange
        url = reverse('user-register')
        data = {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!"
        }
        
        # Act
        response = api_client.post(url, data, format='json')
        
        # Assert
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_registration_password_mismatch(self, api_client):
        # Arrange
        url = reverse('user-register')
        data = {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password123!",
            "confirm_password": "DifferentPassword!"
        }
        
        # Act
        response = api_client.post(url, data, format='json')
        
        # Assert
        if response.status_code != status.HTTP_400_BAD_REQUEST:
            print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not User.objects.filter(email="newuser@example.com").exists()


class TestUserLoginView:
    def test_successful_login(self, api_client, user):
        # Arrange
        url = reverse('user-login')
        data = {
            "username": user.username,
            "password": "password123"
        }
        
        # Act
        response = api_client.post(url, data, format='json')
        
        # Assert
        if response.status_code != status.HTTP_200_OK:
            print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
