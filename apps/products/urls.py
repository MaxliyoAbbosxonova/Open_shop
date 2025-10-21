from django.urls import path
from products.views import ProductListAPIView, ProductDetailAPIView,CategoryListAPIView, CategoryDetailAPIView


urlpatterns = [
    path('list/', ProductListAPIView.as_view(), name='product_list'),
    path('categories/', CategoryListAPIView.as_view(), name='category'),
    path('product/<int:id>/<slug:slug>/',ProductDetailAPIView.as_view() , name='product_detail'),
    path('categories/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category_detail'),

]