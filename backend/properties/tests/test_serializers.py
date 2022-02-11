# properties
from properties.api.serializers import OwnerSerializer, EstateSerializer
from properties.tests.test_models import BasePropertytestCase


class OwnerSerializerTestCase(BasePropertytestCase):
    """
    Casos de prueba para el serializador del modelo Owner
    """

    def setUp(self):

        self.serializer_data = {
            'name': 'Juan Perez',
            'uuid': str(self.person_1.uuid),
            'owner_type': 'Persona',
            'identification': '1056987456'
        }

        self.serializer = OwnerSerializer(instance=self.person_1)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(
            set(data.keys()),
            set(['name', 'uuid', 'owner_type', 'identification']))

    def test_contains_expected_data(self):
        data = self.serializer.data

        self.assertDictEqual(data, self.serializer_data)


class EstateSerializerTestCase(BasePropertytestCase):
    """
    Casos de prueba para el serializador del modelo Estate
    """

    def setUp(self):

        self.serializer_data = {
            'name': 'El encanto',
            'uuid': str(self.estate_2.uuid),
            'estate_type': 'Rural',
            'cadastral_certificate': '1056987456c',
            'estate_registration': '0001-565-b',
            'owners': []
        }

        self.serializer = EstateSerializer(instance=self.estate_2)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(
            set(data.keys()),
            set(['name', 'uuid', 'estate_type', 'cadastral_certificate',
                'owners', 'estate_registration']))

    def test_contains_expected_data(self):
        data = self.serializer.data

        self.assertDictEqual(data, self.serializer_data)

    def test_estate_contains_real_owners_count(self):
        self.estate_2.owners.add(self.person_1)
        self.estate_2.owners.add(self.company_1)

        serializer = EstateSerializer(instance=self.estate_2)

        self.assertEqual(len(serializer.data['owners']), 2)
