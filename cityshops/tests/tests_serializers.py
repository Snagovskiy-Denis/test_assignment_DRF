from django.test import TestCase

from cityshops.models import City
from cityshops.serializers import CitySerializer


class CitySerializerTest(TestCase):

    def test_cannot_save_nameless_city(self):
        serializer = CitySerializer(data={'name': ''})
        self.assertFalse(serializer.is_valid())

    def test_duplicate_city_invalid(self):
        City.objects.create(name='Moscow')
        serializer = CitySerializer(data={'name': 'Moscow'})
        self.assertFalse(serializer.is_valid())

