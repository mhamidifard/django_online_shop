from django.urls import path

from products.views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView, productSearch, \
    GlobalSearchView, ProductCreateView, ProductImageUploadView, ProductUpdateView, ProductDeleteView, \
    ProductVariantView, ProductImageDeleteView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/',ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/images/upload/', ProductImageUploadView.as_view()),
    path('images/<int:pk>/delete/', ProductImageDeleteView.as_view(), name='product-image-delete'),
    path('products/add/',ProductCreateView.as_view(), name='product-add'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('variants/<int:pk>/', ProductVariantView.as_view(), name='variant-update'),

    path('search/', GlobalSearchView.as_view(), name='global-search'),
]