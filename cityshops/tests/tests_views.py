import json

from django.test import TestCase

from cityshops.models import City, Street


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
        street1 = Street.objects.create(city=city, name='Prospekt Stachki')
        street2 = Street.objects.create(city=city, name='Ulitsa Borko')
        street3 = Street.objects.create(city=city, name='Prospekt Lenina')
        response = self.client.get(path=f'/city/{city.id}/street/')
        self.assertEquals(
            json.loads(response.content),
            [
                {'id': street1.id, 'name': street1.name},
                {'id': street2.id, 'name': street2.name},
                {'id': street3.id, 'name': street3.name},
            ]
        )

    def test_get_does_not_return_streets_for_unrequested_city(self):
        city1 = City.objects.create(name='Moscow')
        city2 = City.objects.create(name='Rostov-on-Don')
        street1 = Street.objects.create(city=city1, name='Prospekt Lenina')
        street2 = Street.objects.create(city=city2, name='Prospekt Lenina')

        response = self.client.get(path=f'/city/{city1.id}/street/')
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)

        response_street = json_response[0]
        self.assertEqual(response_street['id'], street1.id)
        self.assertNotEqual(response_street['id'], street2.id)

    def test_post_create_entity_in_database(self):
        self.assertEqual(Street.objects.count(), 0)
        city = City.objects.create(name='Rostov-on-Don')
        data = {'name': 'Prospekt Stachki', 'city': city.id}
        self.client.post(path=f'/city/{city.id}/street/', data=data)
        self.assertEqual(Street.objects.first().name, data['name'])

    def test_post_invalid_data_returns_errors(self):
        city = City.objects.create(name='Rostov-on-Don')
        data = {'name': 'Prospekt Stachki', 'city': 777}
        response = self.client.post(path=f'/city/{city.id}/street/', data=data)
        self.assertEqual(Street.objects.count(), 0)
        self.assertEquals(
            json.loads(response.content),
            {'city': ['Invalid pk "777" - object does not exist.']}
        )


class ShopAPITest(TestCase):

    def test_get_without_data_returns_all_shops_from_database(self):
        self.fail()

    def test_get_with_data_does_search_shops_in_database(self):
        pass

    def test_post_create_entity_in_database(self):
        self.fail()

    def test_post_invalid_data_returns_errors(self):
        self.fail()


# self.client.get(path='/shop/', {'city': city.name, 'street': street.name})
