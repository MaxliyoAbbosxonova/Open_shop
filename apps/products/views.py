from products.models import Category, Product
from products.serializers import (CategoryModelSerializer,
                                  ProductDetailModelSerializer,
                                  ProductModelSerializer)
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
