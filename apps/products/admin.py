from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin
from django.utils.safestring import mark_safe

from products.models import Category, Product, ProductAttribute


@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = ('id', 'name', 'parent', 'icon', 'slug')


class ProductAttributeInline(TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ("key", "value")
    verbose_name = "Attribute"
    verbose_name_plural = "Attributes"


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category')
    inlines = (ProductAttributeInline,)
    readonly_fields = ['image_tag',]

