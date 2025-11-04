from django.core.validators import FileExtensionValidator
from django.db.models import (CASCADE, DecimalField, ForeignKey, ImageField,
                              Model)
from django.db.models.fields import CharField, SlugField
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from shared.models import CreatedBaseModel, UUIDBaseModel


class Category(MPTTModel):
    name = CharField(max_length=255, verbose_name=_("Name"), )
    icon = ImageField(upload_to="categories/", null=True, blank=True)
    slug = SlugField(max_length=255, unique=True, editable=False)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='subcategory')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.id}+'-'=f{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(CreatedBaseModel, UUIDBaseModel):
    name = CharField(verbose_name=_("Name"), max_length=255)
    slug = SlugField(max_length=50, unique=True, editable=False)
    category = ForeignKey('products.Category', CASCADE, to_field='slug', related_name='products',
                          verbose_name=_("Category"))
    description = CKEditor5Field(verbose_name=_("Description"), blank=False, null=False)
    price = DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=2)
    image = ImageField(upload_to='products/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                       null=True, blank=True, verbose_name=_("Image"))

    def image_tag(self):
        return mark_safe('<img src="/directory/%s" width="150" height="150" />' % (self.image.url))

    image_tag.short_description = ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.id}-{self.name}")
            print(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        print(self.slug)
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductAttribute(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name="attributes")
    key = CharField(max_length=100, verbose_name=_("Key"))
    value = CharField(max_length=255, verbose_name=_("Value"))

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
