import base64

import yaml
import requests
import json

from services.auth.endpoints import Endpoints as e


class AbstractUser:
    """Абстрактная модель пользователя. Используется только для унаследования."""

    def __init__(self, user, host, schema):
        self.host = host
        self.schema = schema
        self.user = user
        with open('config.yml', 'r', encoding='utf-8') as file:
            config = yaml.load(file, yaml.SafeLoader)
            self.login = config['users'][self.user]['login']
            self.password = config['users'][self.user]['password']
        self.token = self.__get_token()
        self.basic = self.__get_token_base64()

    def __get_token(self):
        payload = {'username': self.login, 'password': self.password}
        url = f'{self.schema}://{self.host}/{e.AUTH}'

        response = requests.Session().post(url=url, json=payload)
        token = json.loads(response.text)['token']
        return token

    def __get_token_base64(self):
        login = self.login
        passw = self.password
        for_token = f'{login}:{passw}'
        sample_string_bytes = for_token.encode('ascii')
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode('ascii')
        return base64_string


class AdminUser(AbstractUser):

    def __init__(self, user, host, schema):
        super().__init__(user, host, schema)


class TestUser(AbstractUser):
    def __init__(self, user, host, schema):
        super().__init__(user, host, schema)
