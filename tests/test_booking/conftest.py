import pytest
import allure

from services.booking.payloads import generate_body_booking
from utils.helpers import Helper as h
from services.booking.endpoints import Endpoints as e


@pytest.fixture
def create_test_booking(booker_api, logger_test):
    """Фикстура, создающая тестовую сущность и возвращающая ее тело."""
    @allure.step(
        'Создать тестовое бронирование: firstname={firstname}, lastname={lastname}, totalprice={totalprice}, '
        'depositpaid={depositpaid}, checkin={checkin}, checkout={checkout}, additionalneeds={additionalneeds}')
    def _create_test_booking(firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
                             checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast',
                             data_type='json', *args):
        data = generate_body_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
        if data_type == 'xml':
            data_xml = h.convert_dict_to_xml(data)
            logger_test.info(f'Создать тестовую бронь: data {data_xml}.')
            test_booking = booker_api.post(e.POST_BOOKING, data_xml, cont_type='xml', accept_header='xml')
            booking_data = test_booking.text
            elements = h.get_xml_response_data(booking_data, args)
            return elements
        else:
            logger_test.info(f'Создать тестовую бронь: data {data}.')
            test_booking = booker_api.post(e.POST_BOOKING, data)
            test_booking_data = test_booking.json()
            return test_booking_data
    return _create_test_booking


@pytest.fixture
def delete_test_booking(booker_api, logger_test):
    """Фикстура, удаляющая тестовую сущность.
    :param booker_api: id брони для удаления
    """
    @allure.step('Удалить бронь с id {booking_id}')
    def _delete_test_booking(booking_id):
        logger_test.info(f'Удалить тестовую бронь {booking_id}')
        return booker_api.delete(e.DELETE_BOOKING(None, booking_id))
    return _delete_test_booking


@pytest.fixture
def fixture_create_delete_booking_data(create_test_booking, delete_test_booking, request):
    """Фикстура создания дефолтной тестовой брони и ее удаления."""
    def _create_delete(
            firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
            checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast'):
        booking = create_test_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
        booking_id = booking['bookingid']
        booking_data = booking['booking']

        def teardown():
            delete_test_booking(booking_id)
        request.addfinalizer(teardown)
        return booking_id, booking_data
    return _create_delete
