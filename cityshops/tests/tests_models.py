from django.core.exceptions import ValidationError
from django.test import TestCase

from cityshops.models import City


class CityModelTest(TestCase):

    def test_cannot_save_nameless_city(self):
        city = City(name='')
        with self.assertRaises(ValidationError):
            city.save()
            city.full_clean()

    def test_duplicate_city_invalid(self):
        City.objects.create(name='Moscow')
        city = City(name='Moscow')
        with self.assertRaises(ValidationError):
            city.full_clean()

