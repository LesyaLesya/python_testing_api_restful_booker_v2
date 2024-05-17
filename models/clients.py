"""Модуль с классом API клиента."""


import allure
import json
import logging
import requests

from utils.helpers import Helper as h
from utils.headers import Headers


class ApiClient:

    def __init__(self, host, schema):
        """Конструктор класса.

        :param host: адрес хоста
        :param schema: схема
        """
        self.host = host
        self.schema = schema
        self.headers = Headers
        self.session = requests.Session()
        self.logger = logging.getLogger('requests')

    def _get_url(self, path):
        return f'{self.schema}://{self.host}/{path}'

    def get(self, path='', params=None, headers_new=None, accept_header='json'):
        """Возвращает вызов get запроса к API.

        :param path: путь
        :param params: гет параметры
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        """
        headers = headers_new or self.headers.generator(accept=accept_header)
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос GET {url}, headers={headers}, params={params}'):
            res = self.session.get(url=url, params=params, headers=headers)
            h.attach_response_to_log(self.logger, res)
            h.attach_response_to_allure(res)
            return res

    def post(self, path='', data=None, headers_new=None, cont_type='json', accept_header='json'):
        """Возвращает вызов post запроса к API.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        :param cont_type: в каком типе данных отправлять запрос
        """
        headers = headers_new or self.headers.generator(cont_type=cont_type, accept=accept_header)
        if cont_type == 'json':
            data = json.dumps(data)
        else:
            data = data
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос POST {url}, headers={headers}, data={data}'):
            res = self.session.post(url=url, headers=headers, data=data)
            h.attach_response_to_log(self.logger, res)
            h.attach_response_to_allure(res)
            return res
