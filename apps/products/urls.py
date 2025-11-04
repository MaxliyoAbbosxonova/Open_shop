from django.urls import path
from products.views import (CategoryDetailAPIView, CategoryListAPIView,
                            ProductDetailAPIView, ProductListAPIView)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('categories/', CategoryListAPIView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category_detail'),

]
