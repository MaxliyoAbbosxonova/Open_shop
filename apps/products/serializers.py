from products.models import Category, Product
from rest_framework.serializers import ModelSerializer



class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug','icon','parent')


class ProductModelSerializer(ModelSerializer):
    category= CategoryModelSerializer()
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image','slug','category')

class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image','slug','description','category')


