"""Модуль с тестами put запросов - UpdateBooking."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.put_booking
@allure.feature('PUT - UpdateBooking')
class TestUpdateBooking(BaseTest):
    """Тесты метода put /booking/id."""

    @allure.story('Обновление всех параметров')
    @allure.title('Валидные значения у всех полей')
    def test_put_valid_all_fields(
            self, booker_api, fixture_create_delete_booking_data, test_user):
        """Тестовая функция для проверки обновления брони с валидными значениями (все поля).

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data = self.generate_body_booking(
            'Alex', 'Tompson', 13, False, '2023-04-20', '2023-05-05', '')
        response = booker_api.put(self.ep_booker.PUT_BOOKING(booking_id), data, token=test_user.token)
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

    @allure.story('Обновление части параметров')
    @allure.title('Валидные значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Peter', 'Jackson')])
    def test_put_not_all_fields(
            self, booker_api, first, last, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с частью параметров.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в теле запроса firstname
        :param last: передаваемый в теле запроса lastname
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data = {'firstname': first, 'lastname': last}
        response = booker_api.put(self.ep_booker.PUT_BOOKING(booking_id), data)

        self.check.check_response_status_code(response, 400)
        self.check.check_response_time(response)

        get_after_put = booker_api.get(path=self.ep_booker.PUT_BOOKING(booking_id)).json()
        with allure.step(self.check.response_body_msg(get_after_put)):
            assert get_after_put == booking_data, \
                f'Тело до изменения {booking_data}, тело после изменения {get_after_put}'

    @allure.title('Пустое тело')
    def test_put_empty_body(self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с пустым телом.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()
        response = booker_api.put(self.ep_booker.PUT_BOOKING(booking_id), {})

        self.check.check_response_status_code(response, 400)
        self.check.check_response_time(response)

        get_after_put = booker_api.get(path=self.ep_booker.PUT_BOOKING(booking_id)).json()
        with allure.step(self.check.response_body_msg(get_after_put)):
            assert get_after_put == booking_data, \
                f'Тело до изменения {booking_data}, тело после изменения {get_after_put}'

    @allure.title('Обновление брони по невалидному id {value}')
    @pytest.mark.parametrize('value', ['34533424553', '&(*&(*UIU*('])
    def test_put_invalid_id(self, booker_api, value):
        """Тестовая функция для проверки обновления брони по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле id
        """
        data = self.generate_body_booking()
        response = booker_api.put(self.ep_booker.PUT_BOOKING(value), data)
        self.check.check_response_status_code(response, 405)
        self.check.check_response_time(response)

    @allure.story('Обновление всех параметров - urlencoded')
    @allure.title('Валидные значения у всех полей, получение данных в json')
    def test_put_valid_all_fields_urlencoded_accept_json(
            self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с валидными значениями (все поля) в формате urlencoded,
        получение данных в json.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data_urlencoded, data = self.generate_body_booking(
            'Alexia', 'Jackson', 1200, True, '2023-05-01', '2023-05-12', '', convert='urlencoded')
        response = booker_api.put(
            self.ep_booker.PUT_BOOKING(booking_id), data_urlencoded, cont_type='urlencoded', auth_type='basic_auth')
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

    @allure.story('Обновление всех параметров - urlencoded')
    @allure.title('Валидные значения у всех полей, получение данных в xml')
    def test_put_valid_all_fields_urlencoded_accept_xml(
            self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки обновления брони с валидными значениями (все поля) в формате urlencoded,
        получение данных в json.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data()

        data_xml, data = self.generate_body_booking(
            'Test', 'Test123', 1, True, '2024-05-01', '2024-05-12', 'Something', convert='urlencoded')
        response = booker_api.put(
            self.ep_booker.PUT_BOOKING(booking_id), data_xml,
            cont_type='urlencoded', accept_header='xml', auth_type='basic_auth')
        booking_data_new = response.text

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_xml(booking_data_new, self.xsd_schema.GET_BOOKING_SCHEMA_XSD)

        with allure.step(self.check.response_body_msg(booking_data_new)):
            firstname_new, lastname_new, totalprice_new, depositpaid_new, checkin_new, \
            checkout_new, additionalneeds_new = h.get_xml_response_data(
                    booking_data_new, 'firstname', 'lastname', 'totalprice', 'depositpaid',
                    'bookingdates/checkin', 'bookingdates/checkout', 'additionalneeds')

            assert firstname_new == data['firstname'], f'Имя - {firstname_new}'
            assert lastname_new == data['lastname'], f'Фамилия - {lastname_new}'
            assert totalprice_new == str(data['totalprice']), f'Итоговая цена - {totalprice_new}'
            assert depositpaid_new == str(data['depositpaid']).lower(), f'Депозит - {depositpaid_new}'
            assert checkin_new == data['bookingdates']['checkin'], f'Дата заезда - {checkin_new}'
            assert checkout_new == data['bookingdates']['checkout'], f'Дата выезда - {checkout_new}'
            assert additionalneeds_new == data['additionalneeds'], \
                f'additionalneeds - {additionalneeds_new}'
