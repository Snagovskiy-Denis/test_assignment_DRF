from django.test.testcases import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from cityshops.models import City, Street


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
        for city_name in ('Moscow', 'Saint Petersburg', 'Rostov-on-Don'):
            City.objects.create(name=city_name)

        rostov = City.objects.get(name='Rostov-on-Don')
        for street_name in ('Prospekt Stachki', 'Ulitsa Borko', 'Prospekt Lenina'):
            Street.objects.create(name=street_name, city=rostov)

        prospekt_lenina = Street.objects.get(name='Prospekt Lenina')
        # for shop_name in ():
        #     pass

    def get_current_response(self):
        response = self.selenium.find_element_by_class_name(
                'response-info').text
        return response.split('\n\n')

    def get_current_response_body(self):
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

        # John finds his street and adds his shop
        # Shop(name='Funny Kid', city='Rostov-on-Don', street='Prospekt Lenina')
        self.fail('Finish the test!')

        # John checks if his rivals already added their shops
        # for what he sends get request to shop url with search filters
        # /shop/?city=Rostov-on-Don&street=Prospekt%20Lenina
        self.fail('Finish the test!')

        # Satisfied, he goes back to sleep
