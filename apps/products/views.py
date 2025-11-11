from products.models import Category, Highlight, Product, Cart, OrderItem, CartItem
from django_filters.rest_framework import DjangoFilterBackend
from products.serializers import (
    CategoryModelSerializer,
    HighlightModelSerializer,
    ProductDetailModelSerializer,
    ProductModelSerializer, CartModelSerializer, OrderItemModelSerializer, CartItemModelSerializer,
)
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from shared.paginations import CustomPageNumberPagination


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('price', '-price', 'created_at', '-created_at')
    ordering = ('-created_at',)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPageNumberPagination


class HighlightListAPIView(ListCreateAPIView):
    queryset = Highlight.objects.filter().order_by('-created_at')
    serializer_class = HighlightModelSerializer


class CartListAPIView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer


class CartItemListAPIView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer


class OrderListAPIView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer


class OrderItemListAPIView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer
