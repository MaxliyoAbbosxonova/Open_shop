from products.models import Category, Product
from rest_framework.serializers import ModelSerializer


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug','icon','parent')
