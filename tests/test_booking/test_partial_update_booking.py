"""Модуль с тестами patch запросов - PartialUpdateBooking."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.patch_booking
@allure.feature('PATCH - PartialUpdateBooking')
class TestPartialUpdateBooking(BaseTest):
    """Тесты метода patch /booking/id."""

    @allure.story('Обновление части параметров')
    @allure.title('Валидные значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Peter', 'Jackson'), ('Emma', 'Star')])
    def test_patch_valid_firstname_lastname(
            self, booker_api, first, last, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с валидными значениями firstname, lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в теле запроса firstname
        :param last: передаваемый в теле запроса lastname
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data = {'firstname': first, 'lastname': last}
        response = booker_api.patch(self.ep_booker.PATCH_BOOKING(booking_id), data)
        booking_data_new = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_schema)

        with allure.step(self.check.response_body_msg(booking_data_new)):
            assert booking_data_new['firstname'] == first, f'Имя - {booking_data_new["firstname"]}'
            assert booking_data_new['lastname'] == last, f'Фамилия - {booking_data_new["lastname"]}'
            assert booking_data_new['totalprice'] == booking_data['totalprice'], \
                f'Итоговая цена - {booking_data_new["totalprice"]}'
            assert booking_data_new['depositpaid'] == booking_data['depositpaid'], \
                f'Депозит - {booking_data_new["depositpaid"]}'
            assert booking_data_new['bookingdates']['checkin'] == \
                booking_data['bookingdates']['checkin'], \
                f'Дата заезда - {booking_data_new["bookingdates"]["checkin"]}'
            assert booking_data_new['bookingdates']['checkout'] == \
                booking_data['bookingdates']['checkout'], \
                f'Дата выезда - {booking_data_new["bookingdates"]["checkout"]}'
            assert booking_data_new['additionalneeds'] == \
                   booking_data['additionalneeds'], \
                   f'additionalneeds - {booking_data_new["additionalneeds"]}'

    @allure.story('Обновление всех параметров')
    @allure.title('Валидные значения у всех полей')
    def test_patch_valid_all_fields(
            self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с валидными значениями (все поля).

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data = self.generate_body_booking(
            'Andrea', 'Jackson', 232, False, '2022-05-01', '2022-06-01', 'Breakfast, Dinner')
        response = booker_api.patch(self.ep_booker.PATCH_BOOKING(booking_id), data)
        booking_data_new = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_schema)

        with allure.step(self.check.response_body_msg(booking_data_new)):
            assert booking_data_new['firstname'] == data['firstname'], \
                f'Имя - {booking_data_new["firstname"]}'
            assert booking_data_new['lastname'] == data['lastname'], \
                f'Фамилия - {booking_data_new["lastname"]}'
            assert booking_data_new['totalprice'] == data['totalprice'], \
                f'Итоговая цена - {booking_data_new["totalprice"]}'
            assert booking_data_new['depositpaid'] == data['depositpaid'], \
                f'Депозит - {booking_data_new["depositpaid"]}'
            assert booking_data_new['bookingdates']['checkin'] == \
                   data['bookingdates']['checkin'], \
                   f'Дата заезда - {booking_data_new["bookingdates"]["checkin"]}'
            assert booking_data_new['bookingdates']['checkout'] == \
                   data['bookingdates']['checkout'], \
                   f'Дата выезда - {booking_data_new["bookingdates"]["checkout"]}'
            assert booking_data_new['additionalneeds'] == data['additionalneeds'], \
                   f'Пожелания - {booking_data_new["additionalneeds"]}'

    @allure.title('Пустое тело')
    def test_patch_empty_body(self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони при передаче пустого тела.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        response = booker_api.patch(self.ep_booker.PATCH_BOOKING(booking_id), {})
        booking_data_new = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_schema)

        with allure.step(self.check.response_body_msg(booking_data_new)):
            assert booking_data_new['firstname'] == booking_data['firstname'], \
                f'Имя - {booking_data_new["firstname"]}'
            assert booking_data_new['lastname'] == booking_data['lastname'], \
                f'Фамилия - {booking_data_new["lastname"]}'
            assert booking_data_new['totalprice'] == booking_data['totalprice'], \
                f'Итоговая цена - {booking_data_new["totalprice"]}'
            assert booking_data_new['depositpaid'] == booking_data['depositpaid'], \
                f'Депозит - {booking_data_new["depositpaid"]}'
            assert booking_data_new['bookingdates']['checkin'] == \
                   booking_data['bookingdates']['checkin'], \
                f'Дата заезда - {booking_data_new["bookingdates"]["checkin"]}'
            assert booking_data_new['bookingdates']['checkout'] == \
                   booking_data['bookingdates']['checkout'], \
                f'Дата выезда - {booking_data_new["bookingdates"]["checkout"]}'
            assert booking_data_new['additionalneeds'] == booking_data['additionalneeds'], \
                f'Пожелания - {booking_data_new["additionalneeds"]}'

    @allure.title('Обновление брони по невалидному id {value}')
    @pytest.mark.parametrize('value', ['213123', 'tests'])
    def test_patch_invalid_id(self, booker_api, value):
        """Тестовая функция для проверки обновления брони по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передеваемый в урле id
        """
        data = self.generate_body_booking()
        response = booker_api.patch(self.ep_booker.PATCH_BOOKING(value), data)
        self.check.check_response_status_code(response, 405)
        self.check.check_response_time(response)

    @allure.story('Обновление части параметров')
    @allure.title('Валидные значения firstname {first} и lastname {last} - запрос в xml')
    @pytest.mark.parametrize('first, last', [('Peter', 'Jackson'), ('Emma', 'Star')])
    def test_patch_valid_firstname_lastname_xml(
            self, booker_api, first, last, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с валидными значениями firstname, lastname - запрос в xml.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в теле запроса firstname
        :param last: передаваемый в теле запроса lastname
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data_xml, data = self.generate_body_booking(first, last, convert='xml')

        response = booker_api.patch(
            self.ep_booker.PATCH_BOOKING(booking_id), data_xml, cont_type='xml',
            accept_header='xml', auth_type='basic_auth')
        booking_data_new = response.text

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_xml(booking_data_new, self.xsd_schema.GET_BOOKING_SCHEMA_XSD)

        with allure.step(self.check.response_body_msg(booking_data_new)):
            firstname_new, lastname_new, totalprice_new, depositpaid_new, checkin_new, \
            checkout_new, additionalneeds_new = h.get_xml_response_data(
                booking_data_new, 'firstname', 'lastname', 'totalprice', 'depositpaid',
                'bookingdates/checkin', 'bookingdates/checkout', 'additionalneeds')

            assert firstname_new == first, f'Имя - {firstname_new}'
            assert lastname_new == last, f'Фамилия - {lastname_new}'
            assert totalprice_new == str(booking_data['totalprice']), f'Итоговая цена - {totalprice_new}'
            assert depositpaid_new == str(booking_data['depositpaid']).lower(), f'Депозит - {depositpaid_new}'
            assert checkin_new == booking_data['bookingdates']['checkin'], f'Дата заезда - {checkin_new}'
            assert checkout_new == booking_data['bookingdates']['checkout'], f'Дата выезда - {checkout_new}'
            assert additionalneeds_new == booking_data['additionalneeds'], \
                f'additionalneeds - {additionalneeds_new}'

    @allure.story('Проверка заголовков')
    @allure.title('Без токена')
    def test_patch_without_token(
            self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони без токена.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()
        data = self.generate_body_booking()

        response = booker_api.patch(
            self.ep_booker.PATCH_BOOKING(booking_id), data,
            headers_new={'Accept': 'application/json', 'Content-Type': 'application/json'})
        booking_data_new = response.text

        self.check.check_response_status_code(response, 403)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data_new)):
            assert booking_data_new == 'Forbidden', f'Тело ответа без токена - {booking_data_new}'

        response_get = booker_api.get(self.ep_booker.PATCH_BOOKING(booking_id))
        response_after_patch = response_get.json()

        with allure.step(self.check.response_body_msg(response_after_patch)):
            assert response_after_patch == booking_data, \
                f'Тело до изменения {booking_data}, тело после изменения {response_after_patch}'
