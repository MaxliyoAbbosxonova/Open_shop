import uuid

from django.db.models import DateTimeField, Func, Model
from django.db.models.fields import CharField, SlugField, UUIDField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class GenRandomUUID(Func):
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()

    class Meta:
        abstract = True


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), default=uuid.uuid4(), editable=False)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    name = CharField(_("Name"), max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.id}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CreatedBaseModel(UUIDBaseModel):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
