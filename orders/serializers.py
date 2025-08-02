from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart, CartItem



class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.JSONField()
    payment_method = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        user = self.context['request'].user
        try:
            cart = user.cart
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart is empty.")
        if not cart.items.exists():
            raise serializers.ValidationError("Cart has no items.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        cart = user.cart
        cart_items = cart.items.select_related('variant__product').all()

        total_amount = 0
        updated_variants = []

        # Check stock availability
        for item in cart_items:
            variant = item.variant
            if item.quantity > variant.stock:
                raise serializers.ValidationError(
                    f"Insufficient stock for {variant.product.name} - {variant.attributes}."
                )
            total_amount += item.price * item.quantity
            updated_variants.append((variant, item.quantity))

        # Create the order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            shipping_address=validated_data['shipping_address'],
            payment_method=validated_data['payment_method'],
            notes=validated_data.get('notes', ''),
            payment_status='PENDING',
        )

        # Create order items and reduce stock
        for item in cart_items:
            variant = item.variant

            OrderItem.objects.create(
                order=order,
                product_id=str(variant.product.id),
                product_name=variant.product.name,
                quantity=item.quantity,
                price=item.price,
                variant={
                    'id': variant.id,
                    'attributes': variant.attributes,
                }
            )

            # Deduct stock
            variant.stock -= item.quantity
            variant.save()

            # If stock is zero and no other variant has stock, mark product unavailable
            if variant.stock == 0 and not variant.product.variants.exclude(id=variant.id).filter(stock__gt=0).exists():
                variant.product.is_available = False
                variant.product.save()

        # Clear the cart
        cart.items.all().delete()

        return order

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','status','payment_status','total_amount','ordered_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_id',
            'product_name',
            'quantity',
            'price',
            'variant',
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # fields = [
        #     'id',
        #     'user',
        #     'total_amount',
        #     'status',
        #     'shipping_address',
        #     'payment_method',
        #     'payment_status',
        #     'transaction_id',
        #     'ordered_at',
        #     'notes',
        #     'items',
        # ]