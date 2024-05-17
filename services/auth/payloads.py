""" Модуль для генерации данных для запросов. """


import allure
from typing import Any
from pydantic import BaseModel

from utils.helpers import Helper as h


class Credentials(BaseModel):
    username: Any = None
    password: Any = None


@allure.step('Сгенерировать тело для запроса')
def generate_body_auth(username='admin', password='password123', convert=None):
    """Генерация тела для запроса."""
    data = Credentials(username=username, password=password)
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
