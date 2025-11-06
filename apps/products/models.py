from django.core.validators import FileExtensionValidator
from django.db.models import CASCADE, DecimalField, ForeignKey, ImageField, Model
from django.db.models.fields import CharField, IntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from shared.models import CreatedBaseModel, SlugBaseModel, UUIDBaseModel


class Category(MPTTModel, SlugBaseModel):
    icon = ImageField(upload_to="categories/", null=True, blank=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
    order_number=IntegerField(null=True, blank=True)
    


    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(CreatedBaseModel, SlugBaseModel):
    category = ForeignKey('products.Category', CASCADE, to_field='slug', related_name='products',
                          verbose_name=_("Category"))
    description = CKEditor5Field(verbose_name=_("Description"), blank=False, null=False)
    price = DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=2)
    image = ImageField(upload_to='products/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                       null=True, blank=True, verbose_name=_("Image"))

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')



class ProductAttribute(Model):
    product = ForeignKey(Product, CASCADE, related_name="attributes")
    key = CharField(max_length=255, verbose_name=_("Key"))
    value = CharField(max_length=255, verbose_name=_("Value"))

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")


class Highlight(CreatedBaseModel):
    name=CharField(max_length=255, verbose_name=_("Name"))
    image=ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    # width=IntegerField(null=True, blank=True,default=1097)
    # height=IntegerField(null=True, blank=True,default=219)

    def __str__(self):
        return f"Advertising: {self.id}"




