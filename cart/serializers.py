from rest_framework import serializers

from products.models import ProductVariant
from .models import Cart, CartItem


from rest_framework import serializers
from .models import CartItem
from products.models import ProductVariant


class CartItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source='variant.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'variant_name', 'quantity', 'price']
        read_only_fields = ['price']

    def validate(self, attrs):
        print('hi')
        variant = attrs.get('variant')
        quantity = attrs.get('quantity', 1)

        if not variant:
            raise serializers.ValidationError("Variant is required.")

        if variant.stock < quantity:
            raise serializers.ValidationError(f"Only {variant.stock} items in stock.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user)
        variant = validated_data['variant']
        quantity = validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={
                'quantity': quantity,
                'price': variant.price,
            }
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if variant.stock < new_quantity:
                raise serializers.ValidationError(f"Only {variant.stock} items in stock.")
            cart_item.quantity = new_quantity
            cart_item.price = variant.price  # در صورت نیاز، قیمت را به‌روز کنیم
            cart_item.save()
        else:
            if variant.stock < quantity:
                cart_item.delete()
                raise serializers.ValidationError(f"Only {variant.stock} items in stock.")

        return cart_item

    def update(self, instance, validated_data):
        print(validated_data.get('variant'))
        print(instance.variant)
        if instance.variant != validated_data.get('variant'):
            raise serializers.ValidationError(f"you can only update quantity.")
        quantity = validated_data.get('quantity', instance.quantity)

        if instance.variant.stock < quantity:
            raise serializers.ValidationError(f"Only {instance.variant.stock} items in stock.")

        instance.quantity = quantity
        instance.price = instance.variant.price
        instance.save()
        return instance





class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at','total_price' ,'items']
        read_only_fields = ['user', 'created_at', 'updated_at']
    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())