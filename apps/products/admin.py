from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.utils.safestring import mark_safe

from products.models import (
    Branches,
    Cart,
    CartItem,
    Category,
    Highlight,
    Order,
    OrderItem,
    Product,
    ProductAttribute,
)


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


@admin.register(Cart)
class CartModelAdmin(ModelAdmin):
    list_display = ('id', 'user')


@admin.register(CartItem)
class CartItemModelAdmin(ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'cart')


@admin.register(OrderItem)
class OrderItemModelAdmin(ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'order')


@admin.register(Order)
class OrderModelAdmin(ModelAdmin):
    list_display = 'id', 'user', 'status', 'total_amount', 'delivery_type', 'payment_type', 'card_number'

    @admin.display(description='Status')
    def custom_status(self, obj: Order):
        if obj.status == Order.Status.IN_PROGRESS:
            emoji = '⌛️'
        elif obj.status == Order.Status.COMPLETED:
            emoji = '✅'
        else:
            emoji = '❌'
        return f"{emoji} {obj.status}"


@admin.register(Branches)
class BranchModelAdmin(ModelAdmin):
    list_display = ('id', 'name')

    def __str__(self):
        return
