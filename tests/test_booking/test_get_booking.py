"""Модуль с тестами get запросов - GetBooking."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.get_booking
@allure.feature('GET - GetBooking')
class TestGetBooking(BaseTest):
    """Тесты метода get /booking/id."""

    @allure.title('Получение существующей брони по id')
    def test_get_by_exist_id(self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки получения бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.get(path=self.ep_booker.GET_BOOKING(booking_id))
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['firstname'] == booking_test_data['firstname'], \
                f'firstname - {booking_data["firstname"]}'
            assert booking_data['lastname'] == booking_test_data['lastname'], \
                f'lastname - {booking_data["lastname"]}'
            assert booking_data['totalprice'] == booking_test_data['totalprice'], \
                f'totalprice - {booking_data["totalprice"]}'
            assert booking_data['depositpaid'] == booking_test_data['depositpaid'], \
                f'depositpaid - {booking_data["depositpaid"]}'
            assert booking_data['bookingdates']['checkin'] == booking_test_data['bookingdates']['checkin'], \
                f'checkin - {booking_data["bookingdates"]["checkin"]}'
            assert booking_data['bookingdates']['checkout'] == booking_test_data['bookingdates']['checkout'], \
                f'checkout - {booking_data["bookingdates"]["checkout"]}'
            assert booking_data['additionalneeds'] == booking_test_data['additionalneeds'], \
                f'additionalneeds - {booking_data["additionalneeds"]}'

    @allure.title('Получение брони по невалидному id - {value}')
    @pytest.mark.parametrize('value', ['10000000', 'hello', '0'])
    def test_get_by_invalid_id(self, booker_api, value):
        """Тестовая функция для проверки получения бронирования по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в урле id сущностей
        """
        response = booker_api.get(path=self.ep_booker.GET_BOOKING(value))
        response_body = response.text

        self.check.check_response_status_code(response, 404)
        self.check.check_response_time(response, 300)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Not Found', f'Текст ответа - {response_body}'

    @allure.title('Получение существующей брони по id - проверка получения ответа в xml')
    def test_get_by_exist_id_in_xml(
            self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки получения бронирования по существующему id в xml.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.get(
            path=self.ep_booker.GET_BOOKING(booking_id), accept_header='xml')
        booking_data = response.text

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_xml(booking_data, self.xsd_schema.GET_BOOKING_SCHEMA_XSD)

        with allure.step(self.check.response_body_msg(booking_data)):
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds = \
                h.get_xml_response_data(
                    booking_data, 'firstname', 'lastname', 'totalprice', 'depositpaid',
                    'bookingdates/checkin', 'bookingdates/checkout', 'additionalneeds')

            assert firstname == booking_test_data['firstname'], f'firstname - {firstname}'
            assert lastname == booking_test_data['lastname'], f'lastname - {lastname}'
            assert totalprice == str(booking_test_data['totalprice']), f'totalprice - {totalprice}'
            assert depositpaid == str(booking_test_data['depositpaid']).lower(), f'depositpaid - {depositpaid}'
            assert checkin == booking_test_data['bookingdates']['checkin'], f'checkin - {checkin}'
            assert checkout == booking_test_data['bookingdates']['checkout'], f'checkout - {checkout}'
            assert additionalneeds == booking_test_data['additionalneeds'], f'additionalneeds - {additionalneeds}'

    @pytest.mark.parametrize('header', ['text/plain', 'text/html', 'application/pdf'])
    @allure.title('Получение существующей брони с невалидным заголовком')
    def test_get_by_exist_id_with_invalid_headers(
            self, booker_api, fixture_create_delete_booking_data, header):
        """Тестовая функция для проверки получения бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param header: значение заголовка Accept
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.get(path=self.ep_booker.GET_BOOKING(booking_id), headers_new={'Accept': header})
        response_text = response.text

        self.check.check_response_status_code(response, 418)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_text)):
            assert response_text == "I'm a Teapot", \
                f'Ответ при невалидном заголовке Accept: {header} - {response_text}'
