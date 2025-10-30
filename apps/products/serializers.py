from products.models import Category, Product
from rest_framework.serializers import ModelSerializer


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image','slug')

class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image','slug','description','category')




class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug','icon','parent')
