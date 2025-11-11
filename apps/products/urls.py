from django.urls import path
from products.views import (
    CategoryListAPIView,
    HighlightListAPIView,
    ProductDetailAPIView,
    ProductListAPIView, CartListAPIView, CartItemListAPIView, OrderListAPIView, OrderItemListAPIView,
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('categories/', CategoryListAPIView.as_view(), name='category'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('highlights/', HighlightListAPIView.as_view(), name='product_highlight'),
    path('cart/', CartListAPIView.as_view(), name='cart'),
    path('cart_item/', CartItemListAPIView.as_view(), name='cart_item'),
    path('order/', OrderListAPIView.as_view(), name='order'),
    path('order_item/', OrderItemListAPIView.as_view(), name='order_item'),
]
