import json
from datetime import time

from django.test.testcases import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from cityshops.models import City, Street, Shop


class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestData()
        cls.selenium = WebDriver(executable_path='venv/geckodriver')
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # Order and quntity of objects matter
        city_names = ('Moscow', 'Saint Petersburg', 'Rostov-on-Don')
        street_names = ('Prospekt Stachki', 'Ulitsa Borko', 'Prospekt Lenina')
        shop_names = ('Amused Kid', 'Lunar Circle', 'Fabricant')
        for city_name in city_names:
            city = City.objects.create(name=city_name)
            for street_name in street_names:
                street = Street.objects.create(name=street_name, city=city)
                for shop_name in shop_names:
                    closing_hour = 12 if shop_name == 'Fabricant' else 20

                    # This shop will be created through functional test
                    if city_name == 'Rostov-on-Don' and \
                       street_name == 'Prospekt Lenina' and \
                       shop_name == 'Amused Kid':
                        continue

                    Shop.objects.create(
                        name=shop_name, 
                        city=city, 
                        street=street,
                        house_numbers=1,
                        opening_time=time(hour=8),
                        closing_time=time(hour=closing_hour),
                    )

    def get_current_response(self) -> list:
        response = self.selenium.find_element_by_class_name(
            'response-info').text
        return response.split('\n\n')

    def get_current_response_body(self) -> str:
        return self.get_current_response()[-1]
    
    def assertAllIn(self, iterable: tuple, container: str):
        for item in iterable:
            self.assertIn(item, container)


class TestAssignment(FunctionalTest):
    '''Turns natural language of test assignment into testable steps'''

    def test_GET_browse_api_POST_create_entities_and_GET_search_with_filters(
            self):
        # John has heard about new api for cityshop catalog service
        # He goes to check out its homepage to view browsable api
        self.selenium.get(self.live_server_url)

        # His request was successfully satisfied with status code 200
        # response contains links to cities and shops lists
        response_header, response_body = self.get_current_response()

        city_url = f'"city": "{self.live_server_url}/city/"'
        shop_url = f'"shop": "{self.live_server_url}/shop/"'

        self.assertIn('HTTP 200 OK', response_header)
        self.assertIn(city_url, response_body)
        self.assertIn(shop_url, response_body)

        # John wants to see all available cities
        # for that he requests city url and he sees 3 cities
        self.selenium.get(self.live_server_url + '/city/')
        response_body = self.get_current_response_body()

        cities = ('Moscow', 'Saint Petersburg', 'Rostov-on-Don')
        self.assertAllIn(cities, response_body)

        # John wanted to view all Rostov' streets but accidentally
        # misspelled city id. He has got status code 404 in response
        self.selenium.get(self.live_server_url + '/city/4/street/')
        response_header, response_body = self.get_current_response()

        self.assertIn('HTTP 404', response_header)
        self.assertIn('Not found', response_body)

        # He corrects city id and got list of city streets
        self.selenium.get(self.live_server_url + '/city/3/street/')
        response_body = self.get_current_response_body()

        streets = ('Prospekt Stachki', 'Ulitsa Borko', 'Prospekt Lenina')
        self.assertAllIn(streets, response_body)

        # John checks if his rivals already added their shops
        # for what he sends get request to shop url with search filters
        shop_url = '/shop/?city=Rostov-on-Don&street=Prospekt%20Lenina'
        self.selenium.get(self.live_server_url + shop_url)
        response_body = self.get_current_response_body()
        response_json = json.loads(response_body)

        self.assertEqual(len(response_json), 2)
        self.assertNotIn('Amused Kid', response_body)

        # John finds that they alredy did! He wants to adds his shop now
        new_shop_data = {
            'name': 'Amused Kid', 
            'city': 'Rostov-on-Don', 
            'street': 'Prospekt Lenina',
            'house_numbers': 1,
            'opening_time': 8,
            'closing_time': 20,
        }
        form_input_fileds = self.selenium.find_elements_by_tag_name('input')

        for inputbox in form_input_fileds:
            inputbox_name = inputbox.get_attribute('name') 
            if inputbox_name == 'csrfmiddlewaretoken': continue
            value = new_shop_data.get(inputbox_name)
            inputbox.send_keys(value)

        form_input_fileds[-1].send_keys(Keys.ENTER)  # post filled form
        errors = self.selenium.find_element_by_class_name('help-block')
        self.assertEqual(errors.text, '')

        # John recheck shop list for his street and now finds his shop
        shop_url = '/shop/?city=Rostov-on-Don&street=Prospekt%20Lenina'
        self.selenium.get(self.live_server_url + shop_url)
        response_body = self.get_current_response_body()
        response_json = json.loads(response_body)

        self.assertEqual(len(response_json), 3)
        self.assertIn('Amused Kid', response_body)

        # Satisfied, he goes back to sleep
