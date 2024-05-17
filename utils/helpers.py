"""Модуль с общими вспомогательными функциями."""

import allure
import lxml
import urllib
import json

from allure_commons.types import AttachmentType
from dicttoxml import dicttoxml
from lxml.etree import fromstring
from multidimensional_urlencode import urlencode
from urllib.parse import unquote


class Helper:

    @staticmethod
    def attach_response_to_allure(response):
        """Прикрепление тела ответа к allure отчету."""
        try:
            res = json.dumps(response.json(), indent=4)
            allure.attach(body=res, name='API Response', attachment_type=AttachmentType.JSON)
        except json.decoder.JSONDecodeError:
            allure.attach(body=response.content, name='API Response', attachment_type=AttachmentType.TEXT)

    @staticmethod
    def attach_response_to_log(logger, response):
        """Прикрепление тела ответа к лог файлу."""
        logger.info(f'Метод и урл запроса: {response.request.method} {response.request.url}')
        logger.info(f'Заголовки запроса: {response.request.headers}')
        logger.info(f'Заголовки ответа: {response.headers}')
        logger.info(f'Тело запроса: {response.request.body}')
        try:
            logger.info(f'Тело ответа: {response.json()}')
        except json.decoder.JSONDecodeError as err:
            logger.error(f'Невалидный json в ответе. Error: {err}')
            logger.info(f'Тело ответа: {response.content}')

    @staticmethod
    @allure.step('Переконвертировать dict в xml')
    def convert_dict_to_xml(d):
        """Конвертация dict в xml."""
        xml = dicttoxml(d, custom_root='booking', attr_type=False)
        with allure.step(f'Тело запроса - {xml}'):
            return xml

    @staticmethod
    @allure.step('Переконвертировать dict в urlencoded')
    def convert_dict_to_urlencoded(d):
        """Конвертация dict в urlencoded."""
        for k, j in d.items():
            if isinstance(j, str):
                d[k] = urllib.parse.quote(j.encode('utf-8'))
        urlencode_d = urlencode(d)
        body = unquote(urlencode_d)
        with allure.step(f'Тело запроса - {body}'):
            return body

    @staticmethod
    def get_xml_response_data(booking_data, *args):
        """Получение текста элемента XML дерева."""
        try:
            tree = fromstring(booking_data)
        except lxml.etree.XMLSchemaParseError:
            return False
        elements = []
        for i in args:
            with allure.step(f'Получить элемент с xpath={i}'):
                element = tree.xpath(i).pop()
                elements.append(element.text)
        return elements
