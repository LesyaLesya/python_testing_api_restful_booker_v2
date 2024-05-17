"""Модуль с классом API клиента для Auth service."""

from models.clients import ApiClient


class AuthApi(ApiClient):
    """Класс для выполнения запросов к API."""

    def __init__(self, host, schema):
        super().__init__(host, schema)
