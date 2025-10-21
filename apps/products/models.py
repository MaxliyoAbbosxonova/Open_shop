from django.core.validators import FileExtensionValidator
from django.db.models import Model, CASCADE, TextField, DecimalField, DateTimeField, ForeignKey, ImageField
from django.db.models.fields import CharField, SlugField
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from root.settings import CKEDITOR_5_CONFIGS
from shared.models import CreatedBaseModel, UUIDBaseModel


class Category(MPTTModel):
    name = CharField(max_length=255)
    # TODO icon
    slug = SlugField(max_length=255, unique=True, editable=False)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='subcategory')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(CreatedBaseModel, UUIDBaseModel):  # TODO CreatedBasemodel
    # TODO slug = id + name
    name = CharField(max_length=255)
    slug = SlugField(max_length=50, unique=True)
    category = ForeignKey('products.Category', CASCADE, to_field='slug', related_name='products')
    description = CKEditor5Field(blank=False, null=False)
    price = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='products/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                       null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})

# TODO ProductImage

# django form json
# hstore django
