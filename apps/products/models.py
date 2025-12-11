from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db.models import (
    CASCADE,
    DecimalField,
    ForeignKey,
    ImageField,
    Model,
    OneToOneField,
    TextChoices, PositiveIntegerField, SET_NULL,
)
from django.db.models.fields import CharField, IntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from shared.models import CreatedBaseModel, SlugBaseModel


class Category(MPTTModel, SlugBaseModel):
    icon = ImageField(upload_to="categories/", null=True, blank=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

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
    image = ImageField(_("Image"), upload_to='products/%Y/%m/%d',
                       validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                       null=True, blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})

    def convert_to_webp(self):
        is_new_upload = isinstance(self.image.file, (InMemoryUploadedFile, TemporaryUploadedFile))

        if self._state.adding or is_new_upload:
            img = Image.open(self.image)
            img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=85)
            buffer.seek(0)

            filename = f"{self.image.name.split('.')[0]}.webp"
            self.image = ContentFile(buffer.read(), name=filename)
            buffer.close()

    def save(self, *args, **kwargs):
        self.convert_to_webp()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductAttribute(Model):
    product = ForeignKey(Product, CASCADE, related_name="attributes")
    key = CharField(_("Key"), max_length=255)
    value = CharField(_("Value"), max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")


class Highlight(CreatedBaseModel):
    name = CharField(_("Name"), max_length=255)
    image = ImageField(upload_to='products/%Y/%m/%d')

    def __str__(self):
        return f"Advertising: {self.id}"


class Cart(CreatedBaseModel):
    user = OneToOneField('users.User', CASCADE, verbose_name=_("User"), related_name='cart')

    def __str__(self):
        return f"{self.user}"


class CartItem(CreatedBaseModel):
    product = ForeignKey('products.Product', CASCADE, verbose_name=_("Products"))
    quantity = IntegerField(_("Quantity"), default=1)
    cart = ForeignKey(Cart, CASCADE, verbose_name=_("Cart"), related_name='cart_item')

    class Meta:
        verbose_name = _("CartItem")
        verbose_name_plural = _("CartItems")

    def __str__(self):
        return f"{self.id}"


class Branches(CreatedBaseModel):
    name = CharField(_("Name"), max_length=255)
    location = CharField(_("Location"), max_length=255, unique=False)

    # TODO add location

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return f"{self.name}"


class Order(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "canceled", _("Canceled")

    class DeliveryType(TextChoices):
        BRANCH = "branch", _("Branch")
        ADDRESS = "address", _("Address")

    class PaymentType(TextChoices):
        CASH = "cash", _("Cash")
        CARD = "card", _("Card")

    status = CharField(_("Status"), max_length=15, choices=Status.choices, default=Status.IN_PROGRESS)
    user = ForeignKey('users.User', CASCADE, verbose_name=_("User"), related_name='orders')
    total_amount = PositiveIntegerField(_("Total"), default=0)
    delivery_type = CharField(_("Delivery"), max_length=15, choices=DeliveryType.choices, default=DeliveryType.BRANCH)
    region = ForeignKey('products.Region', SET_NULL, null=True, blank=True, verbose_name=_("Region"),
                        related_name='orders')
    district = ForeignKey('products.District', SET_NULL, null=True, blank=True, verbose_name=_("District"),
                          related_name='orders')
    payment_type = CharField(_("Payment Type"), max_length=15, choices=PaymentType.choices)
    address = CharField(_("Address"), max_length=255, blank=True, null=True)
    branch = ForeignKey('products.Branches', SET_NULL, verbose_name=_("Branch"), blank=True, null=True)
    card_number = CharField(_("Card Number"), max_length=255, blank=True, null=True)
    card_date = CharField(_("Card_Date"), max_length=5, blank=True, null=True)
    receiver_first_name = CharField(_("Receiver First Name"), max_length=255, blank=True, null=True)
    receiver_last_name = CharField(_("Receiver Last Name"), max_length=255, blank=True, null=True)
    receiver_phone = CharField(_("Receiver Phone"), max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class OrderItem(CreatedBaseModel):
    product = ForeignKey('products.Product', CASCADE, verbose_name=_("Products"))
    order = ForeignKey('products.Order', CASCADE, verbose_name=_("Order"), related_name='order_items')
    quantity = IntegerField(_("Quantity"), default=1)
    price = DecimalField(_("Price"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}"


class Region(Model):
    name = CharField(_("Name"), max_length=255)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name}"


class District(Model):
    name = CharField(_("Name"), max_length=255)
    region = ForeignKey(Region, CASCADE, verbose_name=_("Region"), related_name='districts')

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
