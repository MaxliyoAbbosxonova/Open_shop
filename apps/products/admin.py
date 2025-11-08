from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.utils.safestring import mark_safe
from products.models import Category, Highlight, Product, ProductAttribute


@admin.register(Highlight)
class HighlightModelAdmin(ModelAdmin):
    list_display = ('id', 'name', 'created_at')


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
class ProductModelAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'price', 'category')
    inlines = (ProductAttributeInline,)
    readonly_fields = ['image_tag', ]

    @admin.display(description="Product Image")
    def image_tag(self, obj: Product):
        return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
