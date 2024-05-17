"""Модуль с классом API клиента для Booking service."""

import allure
import json

from models.clients import ApiClient
from utils.helpers import Helper as h


class BookingApi(ApiClient):
    """Класс для выполнения запросов к API."""

    def __init__(self, host, schema, user):
        super().__init__(host, schema)
        self.user = user

    def patch(
            self, path='', data=None, headers_new=None, cont_type='json',
            accept_header='json', auth_type='cookie', token='', basic=''):
        """Возвращает вызов patch запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        :param cont_type: в каком типе данных отправлять запрос
        :param auth_type: как авторизоваться
        """
        token = token or self.user.token
        basic = basic or self.user.basic
        headers = headers_new or self.headers.generator(
            cont_type=cont_type, accept=accept_header, auth_type=auth_type, token=token, basic=basic)
        if cont_type == 'json':
            data = json.dumps(data)
        else:
            data = data
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос PATCH {url}, headers={headers}, data={data}'):
            res = self.session.patch(url=url, headers=headers, data=data)
            h.attach_response_to_log(self.logger, res)
            h.attach_response_to_allure(res)
            return res

    def put(self, path='', data=None, headers_new=None, cont_type='json',
            accept_header='json', auth_type='cookie', token='', basic=''):
        """Возвращает вызов put запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        :param cont_type: в каком типе данных отправлять запрос
        :param auth_type: как авторизоваться
        """
        token = token or self.user.token
        basic = basic or self.user.basic
        headers = headers_new or self.headers.generator(
            cont_type=cont_type, accept=accept_header, auth_type=auth_type, token=token, basic=basic)
        if cont_type == 'json':
            data = json.dumps(data)
        else:
            data = data
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос PUT {url}, headers={headers}, data={data}'):
            res = self.session.put(url=url, headers=headers, data=data)
            h.attach_response_to_log(self.logger, res)
            h.attach_response_to_allure(res)
            return res

    def delete(self, path='', headers_new=None, cont_type='json', auth_type='cookie', token='', basic=''):
        """Возвращает вызов delete запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: адрес хоста
        :param headers_new: кастомные заголовки
        :param cont_type: в каком типе данных отправлять запрос
        :param auth_type: как авторизоваться
        """
        token = token or self.user.token
        basic = basic or self.user.basic
        headers = headers_new or self.headers.generator(
            cont_type=cont_type, auth_type=auth_type, token=token, basic=basic)
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос DELETE {url}, headers={headers}'):
            res = self.session.delete(url=url, headers=headers)
            h.attach_response_to_log(self.logger, res)
            h.attach_response_to_allure(res)
            return res
