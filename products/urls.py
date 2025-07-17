from django.urls import path

from products.views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView, productSearch, \
    GlobalSearchView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/',ProductDetailView.as_view(), name='product-detail'),
    path('search/', GlobalSearchView.as_view(), name='global-search'),
]