from django.test import TestCase

from cityshops.models import City, Shop, Street
from cityshops.serializers import CitySerializer, ShopSerializer, StreetSerializer


class CitySerializerTest(TestCase):

    def test_cannot_save_nameless_city(self):
        serializer = CitySerializer(data={'name': ''})
        self.assertFalse(serializer.is_valid())

    def test_duplicate_city_invalid(self):
        City.objects.create(name='Moscow')
        serializer = CitySerializer(data={'name': 'Moscow'})
        self.assertFalse(serializer.is_valid())


class StreetSerializerTest(TestCase):

    def test_cannot_save_nameless_street(self):
        city = City.objects.create(name='Moscow')
        data = {'name': '', 'city': city.id}
        serializer = StreetSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_duplicate_street_in_one_city_invalid(self):
        city = City.objects.create(name='Moscow')
        Street.objects.create(name='Prospekt Lenina', city=city)

        data = {'name': 'Prospekt Lenina', 'city': city.id}
        serializer = StreetSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_save_street_with_duplixate_name_if_different_city(self):
        city1 = City.objects.create(name='Moscow')
        city2 = City.objects.create(name='Rostov-on-Don')
        Street.objects.create(name='Prospekt Lenina', city=city1)

        data = {'name': 'Prospekt Lenina', 'city': city2.id}
        serializer = StreetSerializer(data=data)

        self.assertTrue(serializer.is_valid())


class ShopSerializerTest(TestCase):

    def test_cannot_save_with_closing_time_lesser_than_opening_time(self):
        city = City.objects.create(name='Rostov-on-Don')
        street = Street.objects.create(name='Prospekt Lenina', city=city)

        data = {
            'name': 'Amused Kid',
            'city': city.name,
            'street': street.name,
            'house_numbers': 13,
            'opening_time': '08:00:00',
            'closing_time': '07:00:00',
        }
        serializer = ShopSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        error_text = str(serializer.errors.get('non_field_errors'))
        self.assertIn('closing time earlier than opening time', error_text)
