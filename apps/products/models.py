from django.core.validators import FileExtensionValidator
from django.db.models import CASCADE, DecimalField, ForeignKey, ImageField, Model, TextChoices
from django.db.models.fields import CharField, IntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from shared.models import CreatedBaseModel, SlugBaseModel


class Category(MPTTModel, SlugBaseModel):
    icon = ImageField(upload_to="categories/", null=True, blank=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
    order_number = IntegerField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(CreatedBaseModel, SlugBaseModel):
    category = ForeignKey('products.Category', CASCADE, to_field='slug', related_name='products',
                          verbose_name=_("Category"))
    description = CKEditor5Field(verbose_name=_("Description"), blank=False, null=False)
    price = DecimalField(_("Price"), max_digits=10, decimal_places=2)
    image = ImageField(_("Image"),upload_to='products/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                       null=True, blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductAttribute(Model):
    product = ForeignKey(Product, CASCADE, related_name="attributes")
    key = CharField( _("Key"),max_length=255)
    value = CharField(_("Value"),max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")


class Highlight(CreatedBaseModel):
    name = CharField(_("Name"),max_length=255, )
    image = ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return f"Advertising: {self.id}"


class Cart(CreatedBaseModel):
    user = ForeignKey('users.User', CASCADE, verbose_name=_("User"))


class CartItem(CreatedBaseModel):
    products=ForeignKey('products.Product', CASCADE, verbose_name=_("Products"))
    quantity = IntegerField(_("Quantity"),default=1)
    cart=ForeignKey(Cart, CASCADE, verbose_name=_("Cart"))

    class Meta:
        verbose_name = _("CartItem")
        verbose_name_plural = _("CartItems")

class Order(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = _("in_progress"),_("In Progress")
        COMPLETED = _("completed"), _("Completed")
        CANCELLED = _("canceled"), _("Canceled")

    status=CharField(_("Status"),max_length=15,choices=Status.choices, default=Status.IN_PROGRESS )

    user=ForeignKey('users.User', CASCADE, verbose_name=_("User"))
    total_amount=DecimalField(_("Total"), max_digits=10, decimal_places=2)
    

