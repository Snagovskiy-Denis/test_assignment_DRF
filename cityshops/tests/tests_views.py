import json

from django.test import TestCase

from cityshops.models import City


class RootAPITest(TestCase):

    django_test_server_domain = 'http://testserver/'

    def test_get_returns_json_200(self):
        response = self.client.get(path='')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_api_table_of_contents(self):
        response = self.client.get(path='')
        expected = {
            'city': self.django_test_server_domain + 'city/',
            'shop': self.django_test_server_domain + 'shop/',
        }
        self.assertEquals(expected, json.loads(response.content))


class CityAPITest(TestCase):

    def test_get_returns_all_cities_from_database(self):
        city1 = City.objects.create(name='Moscow')
        city2 = City.objects.create(name='Saint Petersburg')
        city3 = City.objects.create(name='Rostov-on-Don')
        response = self.client.get(path='/city/')
        self.assertEquals(
            json.loads(response.content),
            [
                {'id': city1.id, 'name': city1.name},
                {'id': city2.id, 'name': city2.name},
                {'id': city3.id, 'name': city3.name},
            ]
        )

    def test_post_create_entity_in_database(self):
        self.assertEqual(City.objects.count(), 0)
        data = {'name': 'Moscow'}
        self.client.post(path='/city/', data=data)
        self.assertEqual(City.objects.first().name, data['name'])

    def test_post_invalid_data_returns_errors(self):
        data = {'name': ''}
        response = self.client.post(path='/city/', data=data)
        self.assertEqual(City.objects.count(), 0)
        self.assertEquals(
            json.loads(response.content),
            {'name': ['This field may not be blank.']}
        )


class StreetAPITest(TestCase):

    def test_get_returns_all_city_streets_from_database(self):
        city = City.objects.create(name='Rostov-on-Don')


class ShopAPITest(TestCase):
    pass
