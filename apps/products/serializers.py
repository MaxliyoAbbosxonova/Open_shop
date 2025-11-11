from products.fields import RecursiveField
from products.models import Category, Highlight, Product, Cart, CartItem, Order, OrderItem
from rest_framework.serializers import ListSerializer, ModelSerializer


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'slug', 'category')
        ordering = ('-created_at',)


class CategoryModelSerializer(ModelSerializer):
    children = ListSerializer(child=RecursiveField(), source='get_children', read_only=True)
    products = ProductModelSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'icon', 'children', 'products')


class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image', 'slug', 'description', 'category')


class HighlightModelSerializer(ModelSerializer):
    class Meta:
        model = Highlight
        fields = ('id', 'name', 'created_at')


class CartModelSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemModelSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemModelSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
