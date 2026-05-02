from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from product_reviews.models import Review
from product_reviews.serializers import ReviewSerializer, ReviewCreateSerializer

@extend_schema_view(
    post=extend_schema(tags=["product_reviews"], description="Create a product review for authenticated user.")
)
class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
@extend_schema_view(
    get=extend_schema(tags=["product_reviews"], description="List reviews for a product.")
)
class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)

@extend_schema_view(
    delete=extend_schema(tags=["product_reviews"], description="Delete the current user's review.")
)
class ReviewDeleteView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
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
