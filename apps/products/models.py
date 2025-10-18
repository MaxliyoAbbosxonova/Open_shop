from django.db.models import ImageField
from django.db.models import Model, CASCADE, TextField, DecimalField, DateTimeField, ForeignKey
from django.db.models.fields import CharField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel



class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='subcategory')

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(Model):
    category = ForeignKey('products.Category', on_delete=CASCADE, related_name='products')
    name = CharField(max_length=150)
    description = TextField(blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    # image = ImageField(null=False, upload_to='products/%Y/%m/%d')

    def __str__(self):
        return self.name
