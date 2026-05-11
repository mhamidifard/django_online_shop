import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import Group
from products.models import Product
from products.tests.factories import CategoryFactory

pytestmark = pytest.mark.django_db

class TestProductCreateView:
    def test_create_product_authenticated_seller(self, authenticated_client, user):
        # Arrange
        seller_group, _ = Group.objects.get_or_create(name='seller')
        user.groups.add(seller_group)
        
        category = CategoryFactory()
        url = reverse('product-add')
        data = {
            "name": "New Smartphone",
            "slug": "new-smartphone",
            "description": "A very cool smartphone.",
            "category": category.id,
            "is_available": True,
            "variants": [
                {"price": "100.00", "stock": 50, "attributes": {"color": "black"}}
            ]
        }
        
        # Act
        response = authenticated_client.post(url, data, format='json')
        
        # Assert
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(slug="new-smartphone").exists()

    def test_create_product_not_seller(self, authenticated_client, user):
        # Arrange
        category = CategoryFactory()
        url = reverse('product-add')
        data = {
            "name": "New Smartphone",
            "slug": "new-smartphone",
            "description": "A very cool smartphone.",
            "category": category.id,
            "variants": [
                {"price": "100.00", "stock": 50, "attributes": {"color": "black"}}
            ]
        }
        
        # Act
        response = authenticated_client.post(url, data, format='json')
        
        # Assert
        if response.status_code != status.HTTP_403_FORBIDDEN:
            print(response.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
