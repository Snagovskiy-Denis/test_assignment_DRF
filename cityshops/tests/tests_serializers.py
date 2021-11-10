from django.test import TestCase

from cityshops.models import City, Street
from cityshops.serializers import CitySerializer, StreetSerializer


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
