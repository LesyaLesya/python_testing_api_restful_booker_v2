"""Модуль с тестами delete запросов - DeleteBooking."""


import allure
import pytest

from config.base_test import BaseTest


@pytest.mark.delete_booking
@allure.feature('DELETE - DeleteBooking')
class TestDeleteBooking(BaseTest):
    """Тесты метода delete /booking/id."""

    @allure.title('Удаление существующей брони по id с авторизацией через куки')
    def test_delete_by_exist_id_with_cookie(self, booker_api, create_test_booking):
        """Тестовая функция для проверки удаления бронирования по существующему id с авторизацией через куки.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param create_test_booking: фикстура, создающая тестовое бронирование
        """
        booking_id = create_test_booking()['bookingid']
        response = booker_api.delete(path=self.ep_booker.DELETE_BOOKING(booking_id))

        self.check.check_response_status_code(response, 201)
        self.check.check_response_time(response)

        get_after_delete = booker_api.get(path=self.ep_booker.GET_BOOKING(booking_id))
        self.check.check_response_status_code(get_after_delete, 404)

    @allure.title('Удаление существующей брони по id с авторизацией через basic auth')
    def test_delete_by_exist_id_with_basic_auth(self, booker_api, create_test_booking):
        """Тестовая функция для проверки удаления бронирования по существующему id  с авторизацией через basic auth.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param create_test_booking: фикстура, создающая тестовое бронирование
        """
        booking_id = create_test_booking()['bookingid']
        response = booker_api.delete(path=self.ep_booker.DELETE_BOOKING(booking_id), auth_type='basic_auth')

        self.check.check_response_status_code(response, 201)
        self.check.check_response_time(response)

        get_after_delete = booker_api.get(path=self.ep_booker.GET_BOOKING(booking_id))
        self.check.check_response_status_code(get_after_delete, 404)

    @allure.title('Удаление брони по невалидному/несуществующему id - {value}')
    @pytest.mark.parametrize('value', ['abc', '123112'])
    def test_delete_by_invalid_id(self, booker_api, value):
        """Тестовая функция для проверки удаления бронирования по невалидным id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле id
        """
        response = booker_api.delete(path=self.ep_booker.DELETE_BOOKING(value))

        self.check.check_response_status_code(response, 405)
        self.check.check_response_time(response)

    @allure.title('Удаление существующей брони без авторизации')
    def test_delete_without_auth(
            self, booker_api, fixture_create_delete_booking_data):
        """Тестовая функция для проверки удаления бронирования без авторизации.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.delete(
            path=self.ep_booker.DELETE_BOOKING(booking_id), headers_new={'Content-Type': 'application/json'})
        response_text = response.text

        self.check.check_response_status_code(response, 403)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_text)):
            assert response_text == 'Forbidden', f'Тело ответа без авторизации - {response_text}'

        get_after_delete = booker_api.get(path=self.ep_booker.GET_BOOKING(booking_id))
        get_after_delete_body = get_after_delete.json()
        self.check.check_response_status_code(get_after_delete, 200)
        with allure.step(self.check.response_body_msg(get_after_delete_body)):
            assert get_after_delete_body == booking_test_data, \
                f'Бронь после попытки удаления без авторизации {get_after_delete_body}'
