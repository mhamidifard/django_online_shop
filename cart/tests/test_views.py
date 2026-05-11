import pytest
from django.urls import reverse
from rest_framework import status
from cart.models import Cart, CartItem
from products.tests.factories import ProductVariantFactory

pytestmark = pytest.mark.django_db

class TestAddToCartView:
    def test_add_item_to_cart_authenticated(self, authenticated_client, user):
        # Arrange
        variant = ProductVariantFactory()
        url = reverse('add-to-cart')
        data = {
            "variant": variant.id,
            "quantity": 2
        }
        
        # Act
        response = authenticated_client.post(url, data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        cart = Cart.objects.get(user=user)
        assert CartItem.objects.filter(cart=cart, variant=variant).exists()

    def test_add_item_to_cart_unauthenticated(self, api_client):
        # Arrange
        variant = ProductVariantFactory()
        url = reverse('add-to-cart')
        data = {
            "variant": variant.id,
            "quantity": 2
        }
        
        # Act
        response = api_client.post(url, data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
