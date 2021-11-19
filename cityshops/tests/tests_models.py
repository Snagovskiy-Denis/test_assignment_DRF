from unittest.mock import patch

from datetime import time

from django.core.exceptions import ValidationError
from django.test import TestCase

from cityshops.models import City, Shop, Street


class CityModelTest(TestCase):
    def test_cannot_save_nameless_city(self):
        with self.assertRaises(ValidationError):
            City(name='').full_clean()

    def test_duplicate_city_invalid(self):
        City.objects.create(name='Moscow')
        with self.assertRaises(ValidationError):
            City(name='Moscow').full_clean()


class StreetModelTest(TestCase):
    def test_cannot_save_nameless_street(self):
        city = City.objects.create(name='Moscow')
        with self.assertRaises(ValidationError):
            Street(name='', city=city).full_clean()

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


@patch('cityshops.models.timezone.now')
class ShopModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Rostov-on-Don')
        self.street = Street.objects.create(name='Prospekt Lenina',
                                            city=self.city)

    def get_valid_shop(self):
        return Shop(
            name='Amused Kid',
            city=self.city,
            street=self.street,
            house_numbers=13,
            opening_time=time(hour=8),
            closing_time=time(hour=20),
        )

    def test_cannot_save_with_closing_time_lesser_than_opening_time(
            self, mock_now):
        shop = Shop(
            name='Amused Kid',
            city=self.city,
            street=self.street,
            house_numbers=13,
            opening_time=time(hour=8),
            closing_time=time(hour=7),
        )
        with self.assertRaises(ValidationError):
            shop.full_clean()

    def test_is_opened_returns_false_if_now_less_than_opening_time(
            self, mock_now):
        mock_now().time.return_value = time(hour=7, minute=59, second=59)
        shop = self.get_valid_shop()

        self.assertFalse(shop.is_opened())
        self.assertTrue(shop.is_closed())

    def test_is_opened_returns_true_if_now_between_opening_and_closing(
            self, mock_now):
        mock_now().time.return_value = time(hour=12)
        shop = self.get_valid_shop()

        self.assertTrue(shop.is_opened())
        self.assertFalse(shop.is_closed())

    def test_is_opened_returns_false_if_now_greater_than_closing_time(
            self, mock_now):
        mock_now().time.return_value = time(hour=20, second=1)
        shop = self.get_valid_shop()

        self.assertFalse(shop.is_opened())
        self.assertTrue(shop.is_closed())

    def test_is_opened_return_true_if_now_is_opening_time(self, mock_now):
        shop = self.get_valid_shop()
        mock_now().time.return_value = time(hour=8)

        self.assertEqual(shop.opening_time, mock_now().time())
        self.assertTrue(shop.is_opened())
        self.assertFalse(shop.is_closed())

    def test_is_opened_return_false_if_now_is_closing_time(
            self, mock_now):
        shop = self.get_valid_shop()
        mock_now().time.return_value = time(hour=20)

        self.assertEqual(shop.closing_time, mock_now().time())
        self.assertFalse(shop.is_opened())
        self.assertTrue(shop.is_closed())
