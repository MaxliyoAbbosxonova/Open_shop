from rest_framework.views import APIView

from products.models import Category, Product, Highlight
from products.serializers import (
    CategoryModelSerializer,
    ProductDetailModelSerializer,
    ProductModelSerializer, HighlightModelSerializer,
)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)


class HighlightListAPIView(ListCreateAPIView):
    queryset = Highlight.objects.filter().order_by('-created_at')
    serializer_class = HighlightModelSerializer


