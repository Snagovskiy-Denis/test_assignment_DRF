from django.core.exceptions import ValidationError
from django.test import TestCase

from cityshops.models import City, Street


class CityModelTest(TestCase):

    def test_cannot_save_nameless_city(self):
        city = City(name='')
        with self.assertRaises(ValidationError):
            city.save()
            city.full_clean()

    def test_duplicate_city_invalid(self):
        City.objects.create(name='Moscow')
        with self.assertRaises(ValidationError):
            City(name='Moscow').full_clean()


class StreetModelTest(TestCase):

    def test_cannot_save_nameless_street(self):
        city = City.objects.create(name='Moscow')
        street = Street(name='', city=city)
        with self.assertRaises(ValidationError):
            street.save()
            street.full_clean()

    def test_duplicate_street_in_one_city_invalid(self):
        city = City.objects.create(name='Moscow')
        Street.objects.create(name='Prospekt Lenina', city=city)
        with self.assertRaises(ValidationError):
            Street(name='Prospekt Lenina', city=city).full_clean()

    def test_save_street_with_duplicate_name_if_different_city(self):
        city1 = City.objects.create(name='Moscow')
        city2 = City.objects.create(name='Rostov-on-Don') 
        street1 = Street.objects.create(name='Prospekt Lenina', city=city1)
        street2 = Street.objects.create(name='Prospekt Lenina', city=city2)
        self.assertEqual(street1.name, street2.name)
