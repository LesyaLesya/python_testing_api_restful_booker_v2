"""Модуль с тестами запросов - Auth - CreateToken."""


import allure
import pytest

from config.base_test import BaseTest


@pytest.mark.auth
@allure.feature('Auth - CreateToken')
class TestAuthCreateToken(BaseTest):
    """Тесты метода post /auth."""

    @allure.title('Проверка создания валидного токена')
    def test_create_valid_token(self, auth_api):
        """Тестовая функция для проверки создания валидного токена.

        :param auth_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        payload = self.generate_body_auth()
        response = auth_api.post(path=self.ep_auth.AUTH, data=payload)
        data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)
        self.check.validate_json(data, self.auth_token_schema)

    @allure.title('Проверка создания не валидного токена')
    @pytest.mark.parametrize('username, password', [('test', 'test'), (12, 0), (False, None)])
    def test_create_invalid_token(self, auth_api, username, password):
        """Тестовая функция для проверки создания валидного токена.

        :param auth_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        payload = self.generate_body_auth(username=username, password=password)
        response = auth_api.post(path=self.ep_auth.AUTH, data=payload)
        data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(data)):
            assert data['reason'] == 'Bad credentials', f'ответ - {data}'

    @allure.title('Отправка запроса в XML')
    def test_create_token_xml(self, auth_api):
        """Тестовая функция для проверки создания валидного токена в XML.

        :param auth_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        data_xml, data = self.generate_body_auth(convert='xml')
        response = auth_api.post(path=self.ep_auth.AUTH, data=data_xml, cont_type='xml')
        data = response.json()

        self.check.check_response_status_code(response, 200)
        self.check.check_response_time(response)

        with allure.step(self.check.response_body_msg(data)):
            assert data['reason'] == 'Bad credentials', f'ответ - {data}'
