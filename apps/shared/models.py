import uuid

from django.db.models import Model, Func, DateTimeField
from django.db.models.fields import UUIDField


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


class CreatedBaseModel(UUIDBaseModel):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True