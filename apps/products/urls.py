from django.urls import path
from products.views import (
    CategoryListAPIView,
    HighlightListAPIView,
    ProductDetailAPIView,
    ProductListAPIView,
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('categories/', CategoryListAPIView.as_view(), name='category'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('highlights', HighlightListAPIView.as_view(), name='product_highlight'),
    ]
