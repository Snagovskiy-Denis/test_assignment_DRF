import json
from datetime import time
from unittest.mock import patch

from django.test import TestCase

from cityshops.models import City, Street, Shop


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

    def test_post_creates_entity_in_database(self):
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

    def test_post_creates_entity_in_database(self):
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

    def setUp(self):
        '''Insert test data'''
        city_names = ('Moscow', 'Saint Petersburg', 'Rostov-on-Don')
        street_names = ('Prospekt Stachki', 'Ulitsa Borko', 'Prospekt Lenina')
        shop_names = ('Opened 1', 'Opened 2', 'Closed')
        for city_name in city_names:
            city = City.objects.create(name=city_name)
            for street_name in street_names:
                street = Street.objects.create(name=street_name, city=city)
                for shop_name in shop_names:
                    closing_hour = 12 if shop_name == 'Closed' else 20
                    Shop.objects.create(
                        name=shop_name, 
                        city=city, 
                        street=street,
                        house_numbers=1,
                        opening_time=time(hour=8),
                        closing_time=time(hour=closing_hour),
                    )

    def get_json_response(self, data=None) -> dict:
        response = self.client.get(path='/shop/', data=data)
        return json.loads(response.content)

    def test_get_without_data_returns_all_shops_from_database(self):
        response = self.get_json_response()
        self.assertEqual(len(response), 27)

    def test_get_with_data_does_search_shops_in_database(self):
        city = City.objects.get(name='Rostov-on-Don')
        street = Street.objects.get(name='Prospekt Lenina', city=city)
        data = {'city': city.name, 'street': street.name}

        response = self.get_json_response(data=data)
        self.assertEqual(len(response), 3)

        for shop in response:
            self.assertEqual(shop['city'], 'Rostov-on-Don')
            self.assertEqual(shop['street'], 'Prospekt Lenina')

    def test_get_invalid_city_raises_404(self):
        response = self.client.get(path='/shop/', data={'city': 'Utopia'})
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_street_raises_404(self):
        response = self.client.get(path='/shop/', data={'street': 'T17'})
        self.assertEqual(response.status_code, 404)

    def test_get_city(self):
        response = self.get_json_response(data={'city': 'Moscow'})
        self.assertEqual(len(response), 9)

        for shop in response:
            self.assertEqual(shop['city'], 'Moscow')

    def test_get_street(self):
        response = self.get_json_response(data={'street': 'Prospekt Lenina'})
        self.assertEqual(len(response), 9)

        for shop in response:
            self.assertEqual(shop['street'], 'Prospekt Lenina')

    @patch('cityshops.models.timezone.now')
    def test_get_opened_1_returns_opened_shops(self, mock_now):
        mock_now().time.return_value = time(hour=15)
        response = self.get_json_response(data={'opened': 1})
        self.assertEqual(len(response), 18)

    @patch('cityshops.models.timezone.now')
    def test_get_opened_0_returns_closed_shops(self, mock_now):
        mock_now().time.return_value = time(hour=15)
        response = self.get_json_response(data={'opened': 0})
        self.assertEqual(len(response), 9)

    def test_get_invalid_opened_value(self):
        response = self.client.get(path='/shop/', data={'opened': 15})
        self.assertEqual(response.status_code, 404)

    @patch('cityshops.models.timezone.now')
    def test_get_opened_shpos_when_all_shops_are_closed(self, mock_now):
        mock_now().time.return_value = time(hour=23)
        response = self.get_json_response(data={'opened': 1})
        self.assertEqual(len(response), 0)

    @patch('cityshops.models.timezone.now')
    def test_get_city_street_opened_shops(self, mock_now):
        mock_now().time.return_value = time(hour=15)
        data = {'city': 'Moscow', 'street': 'Prospekt Lenina', 'opened': 1}
        response = self.get_json_response(data=data)
        self.assertEqual(len(response), 2)
        for shop in response:
            self.assertNotIn('Closed', shop['name'])

    def test_get_unknown_filter_parametr_raises_404(self):
        response = self.client.get(path='/shop/', data={'rating': 10})
        self.assertEqual(response.status_code, 404)

    def test_post_creates_entity_in_database(self):
        self.assertEqual(len(Shop.objects.all()), 27)
        shop_data = {
            'name': 'Amused Kid', 
            'city': 'Rostov-on-Don', 
            'street': 'Prospekt Lenina',
            'house_numbers': '3d\\6',
            'opening_time': '08:00:00',
            'closing_time': '20:00:00',
        }

        response = self.client.post(path='/shop/', data=shop_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Shop.objects.all()), 28)

    def test_post_invalid_data_returns_errors(self):
        self.assertEqual(len(Shop.objects.all()), 27)
        response = self.client.post(path='/shop/', data={'name': 'Krig'})
        self.assertIn(b'This field is required.', response.content)
        self.assertEqual(len(Shop.objects.all()), 27)
