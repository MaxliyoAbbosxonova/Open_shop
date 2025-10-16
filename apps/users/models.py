import re

from django.contrib.auth.models import AbstractUser
from django.db.models import Model, Func
from django.db.models.fields import CharField, UUIDField
from django.core.exceptions import ValidationError



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
    REQUIRED_FIELDS = ['']


    def check_phone(self):
        digits= re.findall('r\d', self.phone)
        if len(digits)<9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone=''.join(digits)
        self.phone=phone.removeprefix('998')

    def save(self,*,force_insert=False,force_update=False,using=None,update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert,force_update=force_update,using=using)
