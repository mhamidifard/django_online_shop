from rest_framework import serializers

from products.models import Category, Product, ProductVariant


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image_url', 'children']

    def get_children(self, obj):
        children = obj.children.all().order_by('id')
        if children.exists():
            return CategoryListSerializer(children, many=True).data
        return []


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'image_url',
            'children',
        ]

    def get_children(self, obj):
        if obj.children.exists():
            children = obj.children.all().order_by('id')  # یا 'name'
            return CategoryListSerializer(children, many=True).data
        return []

class CategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image_url']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'is_available', 'images']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'price', 'stock', 'attributes']

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'is_available',
            'specifications',
            'images',
            'category',
            'variants',
            'created_at',
            'updated_at'
        ]
