"""Модуль с тестами post запросов - CreateBooking."""

import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - JSON')
class TestCreateBookingJSON(BaseTest):
    """Тесты метода post /booking - JSON."""

    @pytest.fixture
    def fixture_post_booking_firstname(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(firstname=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_lastname(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(lastname=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_totalprice(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(totalprice=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        try:
            booking_data = response.json()
            booking_id = booking_data['bookingid']
        except:
            booking_data = response.text
            booking_id = None
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_deposit(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(depositpaid=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        try:
            booking_data = response.json()
            booking_id = booking_data['bookingid']
        except:
            booking_data = response.text
            booking_id = None
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_checkin(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(checkin=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_checkout(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(checkout=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_additionalneeds(self, booker_api, delete_test_booking, get_params):
        data = self.generate_body_booking(additionalneeds=get_params)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_without_additionalneeds(self, booker_api, delete_test_booking):
        data = self.generate_body_booking(additionalneeds=None)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @pytest.fixture
    def fixture_post_booking_repeat(self, booker_api, delete_test_booking):
        data = self.generate_body_booking()
        response_first = booker_api.post(self.ep_booker.POST_BOOKING, data)
        response_repeat = booker_api.post(self.ep_booker.POST_BOOKING, data)
        booking_data_first = response_first.json()
        booking_data_repeat = response_repeat.json()
        booking_id_first = booking_data_first['bookingid']
        booking_id_repeat = booking_data_repeat['bookingid']
        yield data, response_first, response_repeat
        delete_test_booking(booking_id_first)
        delete_test_booking(booking_id_repeat)

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Peter', 'Maria-Elena', 'Имя Имя', ''])
    def test_post_valid_firstname(self, get_params, fixture_post_booking_firstname):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_firstname

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['firstname'] == get_params, \
                f'Имя - {booking_data["booking"]["firstname"]}'

    @allure.story('Проверка firstname')
    @allure.title('Невалидные значения firstname - {value}')
    @pytest.mark.parametrize('value', [123, True, None])
    def test_post_invalid_firstname(self, booker_api, value):
        """Тестовая функция для проверки создания бронирования с невалидным именем.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в теле запроса варианты для "firstname"
        """
        data = self.generate_body_booking(firstname=value)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname(self, booker_api):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        data = self.generate_body_booking(firstname=None)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка lastname')
    @allure.title('Валидные значения lastname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Иванов', 'Black', 'W', 'Last-name', ''])
    def test_post_valid_lastname(self, get_params, fixture_post_booking_lastname):
        """Тестовая функция для проверки создания бронирования с валидной фамилией.

        :param fixture_post_booking_lastname: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_lastname

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['lastname'] == get_params, \
                f'Фамилия - {booking_data["booking"]["lastname"]}'

    @allure.story('Проверка lastname')
    @allure.title('Невалидные значения lastname - {value}')
    @pytest.mark.parametrize('value', [['sth'], {}, None])
    def test_post_invalid_lastname(self, booker_api, value):
        """Тестовая функция для проверки создания бронирования с невалидной фамилией.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в теле запроса варианты для "lastname"
        """
        data = self.generate_body_booking(lastname=value)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка lastname')
    @allure.title('Не передавать в теле lastname')
    def test_post_without_lastname(self, booker_api):
        """Тестовая функция для проверки создания бронирования без фамилии.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        data = self.generate_body_booking(lastname=None)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка totalprice')
    @allure.title('Валидные значения totalprice - {get_params}')
    @pytest.mark.parametrize('get_params', [123, 1, 566778, 11.2, 0.6])
    def test_post_valid_totalprice(self, get_params, fixture_post_booking_totalprice):
        """Тестовая функция для проверки создания бронирования с валидной ценой.

        :param fixture_post_booking_totalprice: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_totalprice

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['totalprice'] == int(get_params), \
                f'Общая сумма - {booking_data["booking"]["totalprice"]}'

    @allure.story('Проверка totalprice')
    @allure.title('Невалидные значения totalprice - {get_params}')
    @pytest.mark.parametrize('get_params', [False, 'test', None])
    def test_post_invalid_totalprice(self, get_params, fixture_post_booking_totalprice):
        """Тестовая функция для проверки создания бронирования с невалидной ценой.

        :param fixture_post_booking_totalprice: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_totalprice
        self.check.check_response_time(response)

        if get_params is None:
            self.check.check_response_status_code(response, 500)
            with allure.step(self.check.response_body_msg(booking_data)):
                assert booking_data == 'Internal Server Error', f'Тело ответа  - {booking_data}'
        else:
            self.check.check_response_status_code(response, 200)
            self.check.validate_json(booking_data, self.create_schema)
            with allure.step(self.check.response_body_msg(booking_data)):
                assert booking_data['booking']['totalprice'] is None, \
                    f'Тело ответа  - {booking_data}["booking"]["totalprice"]'

    @allure.story('Проверка totalprice')
    @allure.title('Не передавать в теле totalprice')
    def test_post_without_totalprice(self, booker_api):
        """Тестовая функция для проверки создания бронирования без цены.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        data = self.generate_body_booking(totalprice=None)
        response = booker_api.post(self.ep_booker.POST_BOOKING, data)
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка depositpaid')
    @allure.title('Валидные значения depositpaid - {get_params}')
    @pytest.mark.parametrize('get_params', [True, False])
    def test_post_valid_depositpaid(self, get_params, fixture_post_booking_deposit):
        """Тестовая функция для проверки создания бронирования с валидным depositpaid.

        :param fixture_post_booking_deposit:  фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_deposit

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['depositpaid'] == get_params, \
                f'Статус внесения депозита - {booking_data["booking"]["depositpaid"]}'

    @allure.story('Проверка depositpaid')
    @allure.title('Невалидные значения depositpaid - {get_params}')
    @pytest.mark.parametrize('get_params', [123, 0, None, 'test'])
    def test_post_invalid_depositpaid(self, get_params, fixture_post_booking_deposit):
        """Тестовая функция для проверки создания бронирования с валидным depositpaid.

        :param fixture_post_booking_deposit:  фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_deposit

        self.check.check_response_time(response)

        if get_params is None:
            self.check.check_response_status_code(response, 500)
            with allure.step(self.check.response_body_msg(booking_data)):
                assert booking_data == 'Internal Server Error', f'Тело ответа  - {booking_data}'
        else:
            self.check.check_response_status_code(response, 200)
            self.check.validate_json(booking_data, self.create_schema)
            with allure.step(self.check.response_body_msg(booking_data)):
                assert booking_data['booking']['depositpaid'] == bool(get_params), \
                    f'Статус внесения депозита - {booking_data["booking"]["depositpaid"]}'

    @allure.story('Проверка checkin')
    @allure.title('Валидные значения checkin - {get_params}')
    @pytest.mark.parametrize('get_params', ['1900-11-11', '2021-02-11', '2030-06-01'])
    def test_post_valid_checkin(self, get_params, fixture_post_booking_checkin):
        """Тестовая функция для проверки создания бронирования с валидным checkin.

        :param fixture_post_booking_checkin: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_checkin

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkin'] == get_params, \
                f'Дата заезда - {booking_data["booking"]["bookingdates"]["checkin"]}'

    @allure.story('Проверка checkin')
    @allure.title('Невалидные значения checkin - {get_params}')
    @pytest.mark.parametrize('get_params', ['00-00-00', 'tests', ' '])
    def test_post_invalid_checkin(self, get_params, fixture_post_booking_checkin):
        """Тестовая функция для проверки создания бронирования с невалидным checkin.

        :param fixture_post_booking_checkin: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_checkin

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkin'] == '0NaN-aN-aN', \
                f'Дата заезда - {booking_data["booking"]["bookingdates"]["checkin"]}'

    @allure.story('Проверка checkout')
    @allure.title('Валидные значения checkout - {get_params}')
    @pytest.mark.parametrize('get_params', ['1871-01-01', '2021-02-11', '2041-12-31'])
    def test_post_valid_checkout(self, get_params, fixture_post_booking_checkout):
        """Тестовая функция для проверки создания бронирования с валидным checkout.

        :param fixture_post_booking_checkout: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_checkout

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkout'] == get_params, \
                f'Дата выезда - {booking_data["booking"]["bookingdates"]["checkout"]}'

    @allure.story('Проверка additionalneeds')
    @allure.title('Валидные значения additionalneeds - {get_params}')
    @pytest.mark.parametrize('get_params', ['что-то', 'dinner, breakfast', ''])
    def test_post_valid_additionalneeds(self, get_params, fixture_post_booking_additionalneeds):
        """Тестовая функция для проверки создания бронирования с валидным additionalneeds.

        :param fixture_post_booking_additionalneeds: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_additionalneeds

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['additionalneeds'] == get_params, \
                f'Дополнительные пожелания - {booking_data["booking"]["additionalneeds"]}'

    @allure.story('Проверка additionalneeds')
    @allure.title('Не передавать в теле additionalneeds')
    def test_post_without_additionalneeds(self, fixture_post_booking_without_additionalneeds):
        """Тестовая функция для проверки создания бронирования без additionalneeds.

        :param fixture_post_booking_without_additionalneeds: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_without_additionalneeds

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert 'additionalneeds' not in booking_data, \
                f'Дополнительные пожелания - {booking_data["booking"]["additionalneeds"]}'

    @allure.title('Пустое тело запроса')
    def test_post_empty_body(self, booker_api):
        """Тестовая функция для проверки создания бронирования с пустым телом.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        response = booker_api.post(self.ep_booker.POST_BOOKING, {})
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.title('Повторное создание бронирования')
    def test_post_repeat_create_booking(self, fixture_post_booking_repeat):
        """Тестовая функция для проверки повторного создания бронирования.

        :param fixture_post_booking_repeat: фикстура создания и удаления тестовых данных и отправки запроса
        """
        data, response_first, response_repeat = fixture_post_booking_repeat
        response_body_first = response_first.json()
        response_body_repeat = response_repeat.json()

        self.check.check_response_status_code(response_first, 200)
        self.check.check_response_status_code(response_repeat, 200)

        self.check.check_response_time(response_first)
        self.check.check_response_time(response_repeat)

        self.check.validate_json(response_body_first, self.create_schema)
        self.check.validate_json(response_body_repeat, self.create_schema)

        with allure.step(self.check.response_body_msg(response_body_repeat)):
            assert response_body_repeat['booking'] == data, f'Тело ответа  - {response_body_repeat}'


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - XML')
class TestCreateBookingXML(BaseTest):
    """Тесты метода post /booking - XML."""

    @pytest.fixture
    def fixture_post_booking_firstname_xml(self, booker_api, delete_test_booking, get_params):
        data_xml, data = self.generate_body_booking(firstname=get_params, convert='xml')
        response = booker_api.post(self.ep_booker.POST_BOOKING, data_xml, cont_type='xml', accept_header='xml')
        booking_data = response.text
        booking_id, firstname = h.get_xml_response_data(booking_data, 'bookingid', 'booking/firstname')
        yield response, booking_data, booking_id, firstname
        delete_test_booking(booking_id)

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname')
    @pytest.mark.parametrize('get_params', ['Peter', 'Maria', '', 'имя'])
    def test_post_valid_firstname_xml(self, fixture_post_booking_firstname_xml, get_params):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname_xml: фикстура создания и удаления тестовых данных и отправки запроса (xml)
        """

        response, booking_data, booking_id, firstname = fixture_post_booking_firstname_xml

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_xml(booking_data, self.xsd_schema.CREATE_BOOKING_SCHEMA_XSD)

        with allure.step(self.check.response_body_msg(booking_data)):
            if get_params == '':
                assert firstname is None, f'Имя - {firstname}'
            else:
                assert firstname == get_params, f'Имя - {firstname}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname_xml(self, booker_api):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        data_xml, data = self.generate_body_booking(firstname=None, convert='xml')
        response = booker_api.post(self.ep_booker.POST_BOOKING, data_xml, cont_type='xml', accept_header='xml')
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - Urlencoded')
class TestCreateBookingUrlencoded(BaseTest):
    """Тесты метода post /booking - Urlencoded."""

    @pytest.fixture
    def fixture_post_booking_firstname_urlencoded(self, booker_api, delete_test_booking, get_params):
        data_urlencoded, data = self.generate_body_booking(firstname=get_params, convert='urlencoded')
        response = booker_api.post(self.ep_booker.POST_BOOKING, data_urlencoded, cont_type='urlencoded')
        booking_data = response.json()
        booking_id = booking_data['bookingid']
        yield response, booking_data, booking_id
        delete_test_booking(booking_id)

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname')
    @pytest.mark.parametrize('get_params', ['', 'Anna Maria', 'Stacy', 'Аня'])
    def test_post_valid_firstname_urlencoded(
            self, booker_api, fixture_post_booking_firstname_urlencoded, get_params):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname_urlencoded: фикстура создания и удаления тестовых данных и отправки запроса
        """
        response, booking_data, booking_id = fixture_post_booking_firstname_urlencoded

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(booking_data, self.create_schema)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data['booking']['firstname'] == get_params, \
                f'Имя - {booking_data["booking"]["firstname"]}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname_urlencoded(self, booker_api):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        data_urlencoded, data = self.generate_body_booking(firstname=None, convert='urlencoded')
        response = booker_api.post(self.ep_booker.POST_BOOKING, data_urlencoded, cont_type='urlencoded')
        response_body = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - Other data types')
class TestCreateBookingOtherDataType(BaseTest):
    """Тесты метода post /booking - Other data types."""

    @allure.story('Проверка заголовков')
    @allure.title('Content-type: {cont_type}')
    @pytest.mark.parametrize('cont_type', ['text/plain', 'text/html'])
    def test_post_with_invalid_content_type(self, booker_api, cont_type):
        """Тестовая функция для проверки создания бронирования с заголовком Content-type: text/plain.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param cont_type: значение заголовка Content-type
        """
        data = self.generate_body_booking()
        response = booker_api.post(self.ep_booker.POST_BOOKING, data, cont_type=cont_type)
        booking_data = response.text

        self.check.check_response_status_code(response, 500)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data == 'Internal Server Error', \
                f'Тело ответа, если Content-type: {cont_type}  - {booking_data}'

    @allure.story('Проверка заголовков')
    @allure.title('Accept: {accept}')
    @pytest.mark.parametrize('accept', ['application/javascript', 'text/html'])
    def test_post_with_invalid_accept(self, booker_api, accept):
        """Тестовая функция для проверки создания бронирования с заголовком Content-type: text/plain.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param accept: значение заголовка Accept
        """
        data = self.generate_body_booking()
        response = booker_api.post(self.ep_booker.POST_BOOKING, data, accept_header=accept)
        booking_data = response.text

        self.check.check_response_status_code(response, 418)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(booking_data)):
            assert booking_data == "I'm a Teapot", \
                f'Тело ответа, если Accept: {accept}  - {booking_data}'
