from functools import partial

from django.utils.text import slugify
from rest_framework import serializers

from products.models import Category, Product, ProductVariant, ProductImage


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image_url', 'children']

    def get_children(self, obj) -> list[dict]:
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

    def get_children(self, obj) -> list[dict]:
        if obj.children.exists():
            children = obj.children.all().order_by('id')
            return CategoryListSerializer(children, many=True).data
        return []

class CategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image_url']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']  # no 'product' here

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'is_available', 'images']

class ProductVariantListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # mapping: id -> instance
        variant_mapping = {variant.id: variant for variant in instance}
        print(variant_mapping)
        # آپدیت یا ایجاد
        ret = []
        for item in validated_data:
            print(item)
            variant_id = item.get('id', None)
            print(variant_id)
            if variant_id and variant_id in variant_mapping:
                print('yes')
                variant = variant_mapping[variant_id]
                ret.append(self.child.update(variant, item))
            else:
                print('no')
                ret.append(self.child.create(item))
        return ret

class ProductVariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ProductVariant
        fields = ['id',  'price', 'stock','attributes']
        list_serializer_class = ProductVariantListSerializer

    def create(self, validated_data):

        if 'id' in validated_data:
            raise serializers.ValidationError({'id':"ID is not allowed when creating a new variant."})
        validated_data['product'] = self.context['product']
        return super().create(validated_data)

    def validate_id(self, value):
        # فقط اجازه بده اگر در حال آپدیت هستیم
        print(self.instance)
        if type(self.instance)==ProductVariant and value != self.instance.id:
            raise serializers.ValidationError("ID is not changeable.")
        return value


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id','name','slug','description','is_available','specifications','images',
            'category','variants','created_at','updated_at'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'slug', 'description',
            'is_available', 'specifications', 'variants'
        ]
        read_only_fields = ['id']
        extra_kwargs = {'slug': {"required": False}}

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])

        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data['name'])

        request = self.context.get('request')
        validated_data['seller'] = request.user

        product = Product.objects.create(**validated_data)


        variant_serializer = ProductVariantSerializer(
            data=variants_data,
            many=True,
            context={'product': product}
        )
        variant_serializer.is_valid(raise_exception=True)
        variant_serializer.save()

        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if not instance.slug:
            instance.slug = slugify(instance.name)

        instance.save()

        if variants_data is not None:

            variant_serializer = ProductVariantSerializer(
                instance=instance.variants.all(),
                data=variants_data,
                many=True,
                context={'product': instance},
                partial=True
            )
            variant_serializer.is_valid(raise_exception=True)
            variant_serializer.save()

        return instance



