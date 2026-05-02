from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@extend_schema_view(
    get=extend_schema(tags=["cart"], description="Get the authenticated user's cart.")
)
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


@extend_schema_view(
    post=extend_schema(tags=["cart"], description="Add an item to cart or increase quantity.")
)
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_view(
    put=extend_schema(tags=["cart"], description="Update cart item quantity."),
    patch=extend_schema(tags=["cart"], description="Partially update cart item quantity."),
)
class UpdateCartItemView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


@extend_schema_view(
    delete=extend_schema(tags=["cart"], description="Remove an item from the cart.")
)
class RemoveFromCartView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
