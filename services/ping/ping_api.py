"""Модуль с классом API клиента для Ping service."""


from models.clients import ApiClient


class PingApi(ApiClient):
    """Класс для выполнения запросов к API."""

    def __init__(self, host, schema):
        super().__init__(host, schema)
