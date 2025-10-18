from django.contrib import admin
from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','parent')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','created_at')