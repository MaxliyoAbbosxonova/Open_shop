import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import EmailField
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

from shared.models import UUIDBaseModel
from users.models.managers import CustomUserManager


class User(AbstractUser, UUIDBaseModel):
    phone = CharField(max_length=11, unique=True, verbose_name=_("Phone number"))
    email = EmailField(unique=True, null=True, blank=True, verbose_name=_("Email address"))
    username = None

    USERNAME_FIELD = 'phone'
    objects = CustomUserManager()

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
