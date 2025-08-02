from django.urls import path

from orders.views import ConvertCartToOrderView, OrderListView, OrderDetailView

urlpatterns=[

    path('convert-cart-to-order/',ConvertCartToOrderView.as_view(),name='convert-cart-to_order'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

]