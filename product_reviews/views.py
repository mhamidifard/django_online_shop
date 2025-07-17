from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product_reviews.models import Review
from product_reviews.serializers import ReviewSerializer, ReviewCreateSerializer
from products.models import Product

class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)

class ReviewDeleteView(DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You are not allowed to delete this review.")
        instance.delete()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Review deleted successfully."},
            status=status.HTTP_200_OK
        )