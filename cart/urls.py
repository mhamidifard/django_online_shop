from django.urls import path

import cart
from cart.views import CartDetailView

urlpatterns=[
    path('', CartDetailView.as_view(), name='user-cart'),
    path('add/', cart.views.AddToCartView.as_view(), name='add-to-cart'),
    path('update/<int:pk>/', cart.views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('remove/<int:pk>/', cart.views.RemoveFromCartView.as_view(), name='remove-from-cart'),
]