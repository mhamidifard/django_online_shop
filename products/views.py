from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from rest_framework import generics, viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from online_shop.permissions import IsAdmin
from products.models import Category, Product, ProductImage, ProductVariant
from products.permissions import IsSeller, IsSellerOwner
from products.serializers import CategorySerializer, CategoryListSerializer, ProductListSerializer, \
    ProductDetailSerializer, ProductImageSerializer, ProductCreateSerializer, ProductVariantSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view, inline_serializer
from django.core.cache import cache
from .cache_utils import set_cache_with_jitter


@extend_schema_view(
    get=extend_schema(tags=["products"], description="List root categories with nested children.")
)
class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryListSerializer
    paginator_class = None

    def list(self, request, *args, **kwargs):
        cache_key = "categories_root_list"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        set_cache_with_jitter(cache_key, response.data, timeout=3600)
        return response
@extend_schema_view(
    get=extend_schema(tags=["products"], description="Retrieve a category by slug.")
)
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

@extend_schema_view(
    get=extend_schema(tags=["products"], description="List products.")
)
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def list(self, request, *args, **kwargs):
        cache_key = "products_list"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        set_cache_with_jitter(cache_key, response.data, timeout=3600)
        return response

@extend_schema_view(
    get=extend_schema(tags=["products"], description="Retrieve product details with variants and images.")
)
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance_id = self.kwargs.get(self.lookup_field, self.kwargs.get('pk'))
        cache_key = f"product_detail_{instance_id}"
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        set_cache_with_jitter(cache_key, response.data, timeout=3600)
        return response

@extend_schema_view(
    get=extend_schema(
        tags=["products"],
        description="Search products and categories by a free-text query.",
        parameters=[OpenApiParameter(name="q", type=str, location=OpenApiParameter.QUERY, required=True)],
        responses=inline_serializer(
            name="GlobalSearchResponse",
            fields={
                "products": ProductListSerializer(many=True),
                "categories": CategoryListSerializer(many=True),
            },
        ),
    )
)
class GlobalSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        if not query:
            return Response({"products": [], "categories": []})

        products = Product.objects.select_related('category').filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

        categories = Category.objects.filter(name__icontains=query).distinct()

        return Response({
            "products": ProductListSerializer(products, many=True).data,
            "categories": CategoryListSerializer(categories, many=True).data,
        })

class productSearch(APIView):
    def get(self, request, format=None, *args, **kwargs):
        print(request.query_params)
        products = Product.objects.all().filter(**request.query_params.dict())
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


@extend_schema_view(
    post=extend_schema(tags=["products"], description="Create a new product with variants.")
)
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated,IsSeller]

@extend_schema_view(
    post=extend_schema(tags=["products"], description="Upload an image for a product.")
)
class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        # CreateAPIView does not run object-level permission checks automatically.
        self.check_object_permissions(self.request, product)
        serializer.save(product=product)

@extend_schema_view(
    delete=extend_schema(tags=["products"], description="Delete a product image.")
)
class ProductImageDeleteView(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

@extend_schema_view(
    put=extend_schema(tags=["products"], description="Update a product."),
    patch=extend_schema(tags=["products"], description="Partially update a product."),
)
class ProductUpdateView(generics.UpdateAPIView):
    partial=True
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

@extend_schema_view(
    delete=extend_schema(tags=["products"], description="Delete a product.")
)
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

@extend_schema_view(
    get=extend_schema(tags=["products"], description="Retrieve a product variant."),
    put=extend_schema(tags=["products"], description="Update a product variant."),
    patch=extend_schema(tags=["products"], description="Partially update a product variant."),
    delete=extend_schema(tags=["products"], description="Delete a product variant."),
)
class ProductVariantView(generics.RetrieveUpdateDestroyAPIView):
    partial=True
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]
