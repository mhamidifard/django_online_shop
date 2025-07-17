from django.urls import path

from product_reviews.views import ReviewCreateView, ReviewListView, ReviewDeleteView

urlpatterns=[
     path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='product-reviews'),
     path('products/<int:product_id>/reviews/add/',ReviewCreateView.as_view(), name='add-review'),
     path('products/reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete-review'),

 ]