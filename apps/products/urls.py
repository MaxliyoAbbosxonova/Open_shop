from django.urls import path
from products.views import (
    CategoryListAPIView,
    HighlightListAPIView,
    ProductDetailAPIView,
    ProductListAPIView, CartListAPIView, CartItemListCreateAPIView, OrderListCreateAPIView, CartConfirmApiView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('categories/', CategoryListAPIView.as_view(), name='category'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('highlights/', HighlightListAPIView.as_view(), name='product_highlight'),
    path('cart/', CartListAPIView.as_view(), name='cart'),
    path('cart_item/', CartItemListCreateAPIView.as_view(), name='cart_item'),
    path('order/', OrderListCreateAPIView.as_view(), name='order'),
    path('cart/confirm/', CartConfirmApiView.as_view(), name='order_item'),
]
