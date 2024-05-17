""" Модуль с ассертами."""

import logging
import allure
import jsonschema
from lxml import etree
from io import StringIO


class Assertions:
    def __init__(self):
        self.logger = logging.getLogger()

    @allure.step('Провалидировать схему для тела ответа {json_data}')
    def validate_json(self, json_data, base_schema):
        """Валидация json схемы."""
        try:
            schema = base_schema.model_json_schema()
            self.logger.info(f'Валидация схемы для тела {json_data}, схема: {schema}')
            jsonschema.validate(instance=json_data, schema=schema)
        except jsonschema.exceptions.ValidationError:
            assert False
        assert True

    @allure.step('Проверить, что код ответа {code}')
    def check_response_status_code(self, response, code):
        """Проверка кода ответа."""
        self.logger.info(f'Проверка кода ответа {response}, ОР код: {code}')
        assert response.status_code == code, f'Код ответа {response.status_code}, ОР {code}'

    def response_body_msg(self, body):
        self.logger.info(f'Проверить тело ответа - {body}')
        return f'Проверить тело ответа - {body}'

    @allure.step('Провалидировать xml схему для тела ответа {data}')
    def validate_xml(self, data, schema):
        """Валидация xml схемы."""

        try:
            self.logger.info(f'Валидация схемы для тела {data}, схема: {schema}')
            xmlschema = etree.parse(StringIO(schema))
            xmlschema_parse = etree.XMLSchema(xmlschema)

            data_parse = etree.parse(StringIO(data))
            assert xmlschema_parse.validate(data_parse)
        except etree.XMLSchemaParseError:
            assert False

    @allure.step('Проверить, что время ответа меньше {tims_ms} ms')
    def check_response_time(self, response, tims_ms=500):
        """Проверка времени ответа."""

        actual_time = response.elapsed.total_seconds() * 1000
        self.logger.info(f'Проверить время ответа - {actual_time}')
        assert actual_time < tims_ms, f'Время ответа {actual_time}, ОР {tims_ms} ms'
