"""Модуль с тестами get запросов - GetBookingIds."""

import allure
import pytest

from config.base_test import BaseTest


@pytest.mark.get_booking_ids
@allure.feature('GET - GetBookingIds')
class TestGetBookingIds(BaseTest):
    """Тесты метода get /booking."""

    @allure.title('Получение списка всех броней')
    def test_get_all_bookings(self, booker_api):
        """Тестовая функция для проверки получения всех сущностей.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        response = booker_api.get(self.ep_booker.GET_BOOKING_IDS)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_ids_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) != 0, 'Нет ни одной сущности'

    @allure.story('Проверка параметра firstname')
    @allure.title('Валидные значения firstname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Sometest1', 'Olivia12'])
    def test_get_by_valid_firstname(
            self, booker_api, fixture_create_delete_booking_data, get_params):
        """Тестовая функция для проверки получения брони с валидными значениями параметра firstname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data(firstname=get_params)
        payload = {self.query.FIRSTNAME: get_params}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_ids_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 1, f'Количество броней с именем {get_params} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка параметра firstname')
    @allure.title('Несуществующие значения firstname - {value}')
    @pytest.mark.parametrize('value', ['Тест', '13'])
    def test_get_by_invalid_firstname(self, booker_api, value):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметра firstname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр firstname
        """
        payload = {self.query.FIRSTNAME: value}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {value} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка параметра lastname')
    @allure.title('Существующие значения lastname - {get_params}')
    @pytest.mark.parametrize('get_params', ['SomeTest_2', 'Lalala'])
    def test_get_by_valid_lastname(
            self, booker_api, fixture_create_delete_booking_data, get_params):
        """Тестовая функция для проверки получения брони с существующими значениями параметра lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data(lastname=get_params)

        payload = {self.query.LASTNAME: get_params}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_ids_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 1, f'Количество броней с фамилией {get_params} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка параметра lastname')
    @allure.title('Несуществующие значения lastname - {value}')
    @pytest.mark.parametrize('value', ['0', '$$@*:;'])
    def test_get_by_invalid_lastname(self, booker_api, value):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметра lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр lastname
        """
        payload = {self.query.LASTNAME: value}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {value} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка нескольких параметров')
    @allure.title('Существующие значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('test2', 'tester12')])
    def test_get_by_valid_fullname(
            self, booker_api, fixture_create_delete_booking_data, first, last):
        """Тестовая функция для проверки получения брони с существующими значениями параметров firstname и lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_data = fixture_create_delete_booking_data(firstname=first, lastname=last)

        payload = {self.query.FIRSTNAME: first, self.query.LASTNAME: last}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.get_ids_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 1, \
                f'Количество броней с фамилией {last} и именем {first} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка нескольких параметров')
    @allure.title('Несуществующие значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Eric', '0'), ('Test', 'Jones')])
    def test_get_by_invalid_fullname(self, booker_api, first, last):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметров firstname и lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в урле параметр firstname
        :param last: передаваемый в урле параметр lastname
        """
        payload = {self.query.FIRSTNAME: first, self.query.LASTNAME: last}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {first} {last} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка параметра checkin')
    @allure.title('Валидные значения checkin - {value}')
    @pytest.mark.parametrize('value', ['2022-11-15', '2021-02-01'])
    def test_get_by_valid_checkin(self, booker_api, value):
        """Тестовая функция для проверки получения брони с валидными значениями параметра checkin.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр checkin
        """
        payload = {self.query.CHECKIN: value}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert all([booker_api.get(
                path=f'{self.ep_booker.GET_BOOKING_IDS}/{i["bookingid"]}').json()['bookingdates']['checkin']
                        >= value for i in booking_data])

    @allure.story('Проверка параметра checkin')
    @allure.title('Невалидные значения checkin - {value}')
    @pytest.mark.parametrize('value', ['2222', '11-11-2023'])
    def test_get_by_invalid_checkin(self, booker_api, value):
        """Тестовая функция для проверки получения брони с валидными значениями параметра checkin.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр checkin
        """
        payload = {self.query.CHECKIN: value}
        response = booker_api.get(path=self.ep_booker.GET_BOOKING_IDS, params=payload)
        booking_data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert len(booking_data) == 0, \
                f'Количество броней - {len(booking_data)}, тело ответа {booking_data}'
