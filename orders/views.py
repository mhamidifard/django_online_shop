from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer


class ConvertCartToOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "سفارش با موفقیت ایجاد شد", "order_id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class UserOrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,UserOrderPermission]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()


