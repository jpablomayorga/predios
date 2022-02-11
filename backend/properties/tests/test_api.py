# django
from django.urls import resolve

# rest_framework
from rest_framework.test import APITestCase

# properties
from properties.models import Owner, Estate
from properties.tests.test_models import BasePropertytestCase


class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = Owner.objects.create(
            name='pedro Goméz',
            owner_type=0,
            identification='123456')
        cls.owner_2 = Owner.objects.create(
            name='Empresa lactea',
            owner_type=1,
            identification='845454')
        cls.owner_uuid = str(cls.owner.uuid)
        cls.owner2_uuid = str(cls.owner_2.uuid)
        cls.base_api_url = '/api/v1/'


class OwnerAPITestCase(BaseAPITestCase):
    def setUp(self):
        self.owners_url = '{}owners'.format(self.base_api_url)

    def test_retrieve_owner(self):
        """
        Probar que se pueda obtener el detalle de un propietario
        """
        response = self.client.get(f"{self.owners_url}/{str(self.owner.uuid)}")
        self.assertEqual(response.status_code, 200)

    def test_list_owners(self):
        """
        Probar que se pueda conseguir la lista de propietarios
        """
        response = self.client.get(self.owners_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['owner_type'],
                         'Persona')

    def test_owner_list_route(self):
        """
        Probar que la url de la lista de propietarios
        este correctamente direccionada
        """
        route = resolve(self.owners_url)
        self.assertEqual(route.func.__name__, 'OwnerViewSet')

    def test_create_owner(self):
        """
        Probar que se pueda crear un Propietario
        """
        post_data = {
            'name': 'Pablo Marmol',
            'owner_type': 0,
            'identification': '654321',
        }
        response = self.client.post(self.owners_url,
                                    data=post_data,
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_owner_with_registered_identification(self):
        """
        Probar que no se pueda crear un propietario con una
        identificación existente en el sistema
        """
        post_data = {
            'name': 'Pablo Marmol',
            'owner_type': 0,
            'identification': '123456',
        }
        response = self.client.post(self.owners_url,
                                    data=post_data,
                                    format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_owner(self):
        """
        Probar que se pueda editar un Propietario
        """
        patch_data = {
            'name': 'Constructora Azul',
            'owner_type': 1,
        }
        response = self.client.patch(
            f"{self.owners_url}/{self.owner_uuid}",
            data=patch_data,
            format='json')
        self.assertEqual(response.status_code, 202)

        updated_owner = Owner.objects.get(uuid=self.owner_uuid)

        # revisar que los datos del propietario se hayan actualizado
        self.assertEqual(updated_owner.name, 'Constructora Azul')
        self.assertEqual(updated_owner.get_owner_type_display(), 'Empresa')

    def test_update_owner_with_registered_identificaction(self):
        """
        Probar que no se pueda editar un propietario con la
        identificación de otro propietario
        """
        patch_data = {
            'identification': str(self.owner_2.identification),
        }
        response = self.client.patch(
            f"{self.owners_url}/{self.owner_uuid}",
            data=patch_data,
            format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_owner(self):
        """
        Probar que se pueda eliminar un propietario un Propietario
        """
        response = self.client.delete(
            f"{self.owners_url}/{self.owner_uuid}",
            format='json')
        self.assertEqual(response.status_code, 204)


class EstateAPITestCase(BaseAPITestCase, BasePropertytestCase):
    def setUp(self):
        self.estates_url = '{}estates'.format(self.base_api_url)

    def test_retrieve_estate(self):
        """
        Probar que se pueda obtener el detalle de un predio
        """
        response = self.client.get(
            f"{self.estates_url}/{str(self.estate_2.uuid)}")
        self.assertEqual(response.status_code, 200)

    def test_list_estates(self):
        """
        Probar que se pueda conseguir la lista de predios
        """
        response = self.client.get(self.estates_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['estate_type'],
                         'Urbano')

    def test_list_estates_filter_by_name_and_cadastral(self):
        """
        Probar que se pueda conseguir la lista de predios
        con filtros en la url
        """
        request_url = f"{self.estates_url}?cadastral_certificate=1056987456c" \
            "&name=El%20encanto&estate_type=1"
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_estates_filter_by_owner_fields(self):
        """
        Probar que se pueda conseguir la lista de predios
        con filtros de acuerdo a los campos del dueño
        """
        # adicionar los predios a los dueños
        self.person_1.estates.add(self.estate_1)
        self.person_1.estates.add(self.estate_2)

        request_url = f"{self.estates_url}?owner_name=Juan%20Perez" \
            "&owner_identification=1056987456"
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_estate_list_route(self):
        """
        Probar que la url de la lista de predios
        este correctamente direccionada
        """
        route = resolve(self.estates_url)
        self.assertEqual(route.func.__name__, 'EstateViewSet')

    def test_create_estate(self):
        """
        Probar que se pueda crear un Predio y asignarle
        propietarios
        """
        post_data = {
            'name': 'La palma',
            'estate_type': 1,
            'cadastral_certificate': '1056987456z',
            'estate_registration': '0001-565-h',
            'owners': [
                str(self.person_1.uuid),
                str(self.company_1.uuid)
            ]
        }
        response = self.client.post(self.estates_url,
                                    data=post_data,
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_estate_without_owners(self):
        """
        Probar que se pueda crear un Predio sin asignarle
        propietarios
        """
        post_data = {
            'name': 'La palma',
            'estate_type': 1,
            'cadastral_certificate': '1056987456z',
            'estate_registration': '0001-565-h',
            'owners': [],
        }
        response = self.client.post(self.estates_url,
                                    data=post_data,
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_estate_with_registered_estate_registration(self):
        """
        Probar que no se pueda crear un predio con una
        matricula inmobiliria existente en el sistema
        """
        post_data = {
            'name': 'La palma',
            'estate_type': 1,
            'cadastral_certificate': '1056987456z',
            'estate_registration': '0001-565-b',
        }
        response = self.client.post(self.estates_url,
                                    data=post_data,
                                    format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_owner(self):
        """
        Probar que se pueda editar un Predio
        """
        estate_id = str(self.estate_2.uuid)
        patch_data = {
            'name': 'El pino',
            'owners': [
                str(self.person_1.uuid),
            ]
        }
        response = self.client.patch(
            f"{self.estates_url}/{estate_id}",
            data=patch_data,
            format='json')
        self.assertEqual(response.status_code, 202)

        updated_estate = Estate.objects.get(uuid=estate_id)

        # revisar que los datos del propietario se hayan actualizado
        self.assertEqual(updated_estate.name, 'El pino')
        self.assertEqual(updated_estate.owners.all().count(), 1)

    def test_update_estate_with_registered_cadastral_certificate(self):
        """
        Probar que no se pueda editar un predio con la
        identificación de otro predio
        """
        patch_data = {
            'cadastral_certificate': str(self.estate_2.cadastral_certificate),
        }
        response = self.client.patch(
            f"{self.estates_url}/{str(self.estate_1.uuid)}",
            data=patch_data,
            format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_owner(self):
        """
        Probar que se pueda eliminar un predio, incluso
        si tiene propietarios
        """
        estate_id = str(self.estate_2.uuid)
        self.estate_2.owners.add(self.person_1)
        self.estate_2.owners.add(self.company_1)
        response = self.client.delete(
            f"{self.estates_url}/{estate_id}",
            format='json')
        self.assertEqual(response.status_code, 204)
