import re

from django.contrib.auth.models import AbstractUser
from django.db.models import Model, Func, CASCADE, TextField, DecimalField, DateTimeField, ForeignKey
from django.db.models.fields import CharField, UUIDField
from django.core.exceptions import ValidationError
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class GenRandomUUID(Func):
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), editable=False)

    class Meta:
        abstract = True

class User(AbstractUser,UUIDBaseModel):
    phone =CharField(max_length=11, unique=True)
    email = None
    username = None


    USERNAME_FIELD = 'phone'


    def check_phone(self):
        digits= re.findall(r'\d', self.phone)
        if len(digits)<9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone=''.join(digits)
        self.phone=phone.removeprefix('998')

    def save(self,*,force_insert=False,force_update=False,using=None,update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert,force_update=force_update,using=using)


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='subcategory')

    class MPTTMeta:
        order_insertion_by = ['name']

class Product(Model):
    category = ForeignKey('users.Category', on_delete=CASCADE, related_name='products'
    )
    name = CharField(max_length=150)
    description = TextField(blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

