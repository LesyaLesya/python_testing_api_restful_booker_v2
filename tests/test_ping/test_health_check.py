"""Модуль с тестами запросов - Ping - HealthCheck."""


import allure
import pytest

from config.base_test import BaseTest


@pytest.mark.ping
@allure.feature('Ping - HealthCheck')
class TestPingHealthCheck(BaseTest):
    """Тесты метода get /ping."""

    @allure.title('Проверка жизни сервиса')
    def test_health_check(self, ping_api):
        """Тестовая функция для проверки состояния сервиса.

        :param ping_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        """
        response = ping_api.get(path=self.ep_ping.PING)

        self.check.check_response_status_code(response, 201)
        self.check.check_response_time(response, 1000)
