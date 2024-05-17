""" Модуль для генерации данных для запросов. """


import allure
from typing import Any
from pydantic import BaseModel

from utils.helpers import Helper as h


class BookingDates(BaseModel):
    checkin: Any = None
    checkout: Any = None


class BookingData(BaseModel):
    firstname: Any = None
    lastname: Any = None
    totalprice: Any = None
    depositpaid: Any = None
    bookingdates: BookingDates = None
    additionalneeds: Any = None


@allure.step('Сгенерировать тело для запроса')
def generate_body_booking(
        firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
        checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast',
        convert=None):
    """Генерация тела для запроса."""
    data = BookingData(
        firstname=firstname, lastname=lastname, totalprice=totalprice,
        depositpaid=depositpaid,
        bookingdates=BookingDates(checkin=checkin, checkout=checkout),
        additionalneeds=additionalneeds)
    d = data.model_dump(exclude_none=True)
    if convert == 'xml':
        x = h.convert_dict_to_xml(d)
        with allure.step(f'Тело запроса - {x}'):
            return x, d
    if convert == 'urlencoded':
        u = h.convert_dict_to_urlencoded(d)
        with allure.step(f'Тело запроса - {u}'):
            return u, d
    with allure.step(f'Тело запроса - {d}'):
        return d
