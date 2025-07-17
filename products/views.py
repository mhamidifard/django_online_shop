from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Category, Product
from products.serializers import CategorySerializer, CategoryListSerializer, ProductListSerializer, \
    ProductDetailSerializer
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


