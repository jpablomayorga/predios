# django
from django.test import TestCase

# properties
from properties.models import Owner, Estate


class BasePropertytestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.person_1 = Owner.objects.create(
            name='Juan Perez',
            owner_type=0,
            identification='1056987456'
        )
        cls.company_1 = Owner.objects.create(
            name='Ecopetrol',
            owner_type=1,
            identification='1056987456a'
        )
        cls.estate_1 = Estate.objects.create(
            name='calle 7 # 14-64',
            estate_type=0,
            cadastral_certificate='1056987456b',
            estate_registration='0001-565-a'
        )
        cls.estate_2 = Estate.objects.create(
            name='El encanto',
            estate_type=1,
            cadastral_certificate='1056987456c',
            estate_registration='0001-565-b'
        )
        cls.estate_3 = Estate.objects.create(
            name='Las delicias',
            estate_type=1,
            cadastral_certificate='1056987456d',
            estate_registration='0001-565-c'
        )


class OwnerModelTestCase(BasePropertytestCase):
    """
    Casos de prueba para el modelo Owner
    """
    def setUp(self):
        self.person_1.estates.add(self.estate_1)
        self.person_1.estates.add(self.estate_2)

    def test_owner_basic(self):
        """
        Prueba la funcionalidad basica del modelo Owner
        """
        self.assertEqual(self.person_1.name, 'Juan Perez')
        self.assertEqual(self.person_1.identification, '1056987456')
        # probar que los valores enumerados muestren la cadena correspondiente
        self.assertEqual(self.person_1.get_owner_type_display(), 'Persona')

    def test_object_name_is_name_dash_identification(self):
        """
            Probar que el nombre del objeto sea el que se definio en la
            función __str__ de la clase
        """
        expected_object_name = '{} - {}'.format(
            self.person_1.name, self.person_1.identification)
        self.assertEqual(str(self.person_1), expected_object_name)

    def test_owner_has_multiple_estates(self):
        """
        Probar que un propietario pueda tener varios predios
        """
        self.assertEqual(self.person_1.estates.all().count(), 2)


class EstateModelTestCase(BasePropertytestCase):
    """
    Casos de prueba para el modelo Estate
    """
    def setUp(self):
        self.estate_2.owners.add(self.person_1)
        self.estate_2.owners.add(self.company_1)

    def test_estate_basic(self):
        """
        Prueba la funcionalidad basica del modelo Estate
        """
        self.assertEqual(self.estate_2.name, 'El encanto')
        self.assertEqual(self.estate_2.cadastral_certificate, '1056987456c')
        self.assertEqual(self.estate_2.estate_registration, '0001-565-b')
        # probar que los valores enumerados muestren la cadena correspondiente
        self.assertEqual(self.estate_2.get_estate_type_display(), 'Rural')

    def test_object_name_is_name_dash_estate_registration(self):
        """
            Probar que el nombre del objeto sea el que se definio en la
            función __str__ de la clase
        """
        expected_object_name = '{} - {}'.format(
            self.estate_2.name, self.estate_2.estate_registration)
        self.assertEqual(str(self.estate_2), expected_object_name)

    def test_estate_has_multiple_owners(self):
        """
        Probar que un predio pueda tener varios dueños
        """
        self.assertEqual(self.estate_2.owners.all().count(), 2)
