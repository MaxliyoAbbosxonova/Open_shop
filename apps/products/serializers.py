from products.fields import RecursiveField
from products.models import Category, Highlight, Product
from rest_framework.serializers import ListSerializer, ModelSerializer


class CategoryModelSerializer(ModelSerializer):
    children =ListSerializer(child=RecursiveField(),source='get_children', read_only=True)
    # products=ProductModelSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('name', 'slug', 'icon', 'children',)


class ProductModelSerializer(ModelSerializer):
    category=CategoryModelSerializer()
    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'slug', 'category')
        ordering = ('-created_at',)



class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image', 'slug', 'description', 'category')


class HighlightModelSerializer(ModelSerializer):
    class Meta:
        model = Highlight
        fields=('id','name','created_at')
