from django.db.models import Model, Func
from django.db.models.fields import UUIDField


class GenRandomUUID(Func):
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()

    class Meta:
        abstract = True


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), editable=False)

    class Meta:
        abstract = True
