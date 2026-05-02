from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers

from online_shop.permissions import IsAdmin
from orders.models import Order
from orders.permissions import UserOrderPermission
from orders.serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer, \
    OrderStatusUpdateSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["orders"],
        description="Convert authenticated user's cart into an order.",
        request=OrderCreateSerializer,
        responses=inline_serializer(
            name="ConvertCartToOrderResponse",
            fields={
                "message": serializers.CharField(),
                "order_id": serializers.IntegerField(),
            },
        ),
        examples=[
            OpenApiExample(
                "Create order payload",
                value={
                    "shipping_address": {"city": "Tehran", "street": "Main St"},
                    "payment_method": "COD",
                    "notes": "Leave at door",
                },
                request_only=True,
            )
        ],
    )
)
class ConvertCartToOrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "سفارش با موفقیت ایجاد شد", "order_id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(tags=["orders"], description="List authenticated user's orders.")
)
class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@extend_schema_view(
    get=extend_schema(tags=["orders"], description="Retrieve order details.")
)
class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,UserOrderPermission]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

@extend_schema_view(
    patch=extend_schema(tags=["orders"], description="Update order status (admin only).")
)
class OrderStatusUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    serializer_class = OrderStatusUpdateSerializer
    queryset = Order.objects.all()
    http_method_names = ['patch']
