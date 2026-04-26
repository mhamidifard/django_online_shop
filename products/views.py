from django.db.models import Q
from django.shortcuts import render
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



# Create your views here.
class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryListSerializer
    paginator_class = None
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

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


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated,IsSeller]

class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        # CreateAPIView does not run object-level permission checks automatically.
        self.check_object_permissions(self.request, product)
        serializer.save(product=product)

class ProductImageDeleteView(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

class ProductUpdateView(generics.UpdateAPIView):
    partial=True
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]

class ProductVariantView(generics.RetrieveUpdateDestroyAPIView):
    partial=True
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated & (IsSellerOwner | IsAdmin)]
