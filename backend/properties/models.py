# django
from django.db import models

# core
from core.models import TimeStampedModel, UniqueIdentifierModel


class Owner(TimeStampedModel, UniqueIdentifierModel):
    """
    Modelo que representa el dueño de un predio
    """

    PERSON = 0
    COMPANY = 1

    OWNER_TYPE = (
        (PERSON, 'Persona'),
        (COMPANY, 'Empresa'),
    )

    name = models.CharField(max_length=200, verbose_name="Nombre propietario")
    owner_type = models.SmallIntegerField(choices=OWNER_TYPE)
    identification = models.CharField(
        max_length=50,
        verbose_name="Identificación",
        unique=True)

    class Meta:
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'
        ordering = ['created']

    def __str__(self):
        return "{} - {}".format(self.name, self.identification)


class Estate(TimeStampedModel, UniqueIdentifierModel):
    """
    Modelo que representa un predio urbano o rural
    """

    URBAN = 0
    RURAL = 1

    ESTATE_TYPE = (
        (URBAN, 'Urbano'),
        (RURAL, 'Rural'),
    )

    name = models.CharField(max_length=200, verbose_name="Identificación")
    estate_type = models.SmallIntegerField(choices=ESTATE_TYPE)
    cadastral_certificate = models.CharField(
        max_length=50,
        verbose_name="Cédula catastral",
        unique=True)
    owners = models.ManyToManyField(
        Owner,
        related_name='estates',
        null=True,
        blank=True)
    estate_registration = models.CharField(
        max_length=50,
        verbose_name="Matricula inmobiliaria",
        unique=True)

    class Meta:
        verbose_name = 'Predio'
        verbose_name_plural = 'Predios'
        ordering = ['created']

    def __str__(self):
        return "{} - {}".format(self.name, self.estate_registration)
