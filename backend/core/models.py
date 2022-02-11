# django
from django.db import models

# python
import uuid as uuid_lib


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que permite manejar Modelos que tiene fecha
    de creación y modificación
    """
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación')
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación')

    class Meta:
        abstract = True


class UniqueIdentifierModel(models.Model):
    """
    Modelo abstracto que permite generar la identifición única para cada
    instancia de un modelo
    """
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)

    class Meta:
        abstract = True
