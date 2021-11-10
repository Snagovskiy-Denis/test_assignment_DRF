from django.test import TestCase


class RootAPITest(TestCase):

    base_url = 'http://127.0.0.1:8000/'

    def test_get_returns_json_200(self):
        response = self.client.get(path='')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_api_table_of_contents(self):
        response = self.client.get(path='')
        expected = {
            'city': self.base_url + 'city/',
            'shop': self.base_url + 'shop/',
        }
        self.assertEquals(expected, response.content)


class CityAPITest(TestCase):
    pass


class StreetAPITest(TestCase):
    pass


class ShopAPITest(TestCase):
    pass
