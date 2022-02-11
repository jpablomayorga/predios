# properties
from properties.models import Estate, Owner

# rest_framework
from rest_framework.serializers import (
    CharField,
    ModelSerializer)


class OwnerSerializer(ModelSerializer):
    """
    Serializador para el modelo Owner
    """
    # mostrar los valores del choice en el serializador
    owner_type = CharField(source='get_owner_type_display')
    uuid = CharField(read_only=True)

    class Meta:
        model = Owner
        fields = ['name', 'uuid', 'owner_type', 'identification']


class OwnerUUIDSerializer(ModelSerializer):
    """
    Serializador para obtener el uuid del dueño
    """
    class Meta:
        model = Owner
        fields = ['uuid']


class EstateSerializer(ModelSerializer):
    """
    Serializador para el modelo Estate
    """
    # mostrar los valores del choice en el serializador
    # para el tipo de propietario
    estate_type = CharField(source='get_estate_type_display')
    owners = OwnerUUIDSerializer(many=True)
    uuid = CharField(read_only=True)

    class Meta:
        model = Estate
        fields = [
            'name',
            'uuid',
            'estate_type',
            'cadastral_certificate',
            'owners',
            'estate_registration'
        ]
