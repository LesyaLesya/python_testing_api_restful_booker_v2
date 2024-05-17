""" Модуль с заголовками."""


class Headers:

    @staticmethod
    def generator(cont_type=None, accept=None, auth_type=None, token=None, basic=None):
        """Генерация заголовков запроса"""
        headers = {}
        if cont_type == 'json':
            headers['Content-Type'] = 'application/json'
        elif cont_type == 'xml':
            headers['Content-Type'] = 'text/xml'
        elif cont_type == 'urlencoded':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        elif cont_type is None:
            pass
        else:
            headers['Content-Type'] = cont_type

        if accept == 'json':
            headers['Accept'] = 'application/json'
        elif accept == 'xml':
            headers['Accept'] = 'application/xml'
        elif accept is None:
            pass
        else:
            headers['Accept'] = accept

        if auth_type == 'cookie':
            headers['Cookie'] = f'token={token}'
        if auth_type == 'basic_auth':
            headers['Authorization'] = f'Basic {basic}'
        return headers
