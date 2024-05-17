"""Модуль с фикстурами."""

import logging
import pytest
import yaml

from services.booking.booking_api import BookingApi
from services.auth.auth_api import AuthApi
from services.ping.ping_api import PingApi
from models.users import AdminUser, TestUser


def pytest_addoption(parser):
    parser.addoption('--schema', action='store', default='https', choices=['https', 'http'])
    parser.addoption('--host', action='store', default='default')
    parser.addoption('--user', action='store', default='admin')


@pytest.fixture(scope='session')
def cfg():
    with open('config.yml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.SafeLoader)
    return config


@pytest.fixture(scope='session')
def get_host(cfg, request):
    r = request.config.getoption('--host')
    return cfg['host'][r]


@pytest.fixture(scope='session')
def get_schema(cfg, request):
    r = request.config.getoption('--schema')
    return cfg['schema'][r]


@pytest.fixture(scope='session')
def admin_user(get_host, get_schema):
    return AdminUser('admin', get_host, get_schema)


@pytest.fixture(scope='session')
def test_user(get_host, get_schema):
    return TestUser('test', get_host, get_schema)


@pytest.fixture(scope='session')
def get_user(request, admin_user, test_user):
    get_user = request.config.getoption('--user')
    d = {'admin': admin_user, 'test': test_user}
    return d[get_user]


@pytest.fixture(scope='session', autouse=True)
def logger_test():
    logger = logging.getLogger('testing')
    return logger


@pytest.fixture(autouse=True)
def log_test_description(request, logger_test):
    logger_test.info(f'___Test "{request.node.nodeid}" START')
    yield
    logger_test.info(f'___Test "{request.node.nodeid}" COMPLETE')


@pytest.fixture(scope='module', autouse=True)
def log_module_description(request, logger_test):
    logger_test.info(f'_____START testing module {request.node.name}')
    yield
    logger_test.info(f'_____STOP testing module {request.node.name}')


@pytest.fixture
def get_params(request):
    return request.param


@pytest.fixture(scope='session')
def booker_api(get_host, get_schema, logger_test, get_user):
    """Фикстура, создающая и возвращающая экземпляр api клиента Booking."""
    host = get_host
    schema = get_schema
    logger_test.info(
        f'Инициализация экземпляра АПИ клиента Booking: host {host}, '
        f'schema {schema},  юзер {get_user.login}')
    return BookingApi(host, schema, get_user)


@pytest.fixture(scope='session')
def auth_api(get_host, get_schema, logger_test):
    """Фикстура, создающая и возвращающая экземпляр api клиента Auth."""
    host = get_host
    schema = get_schema
    logger_test.info(
        f'Инициализация экземпляра АПИ клиента Auth: host {host}, '
        f'schema {schema}')
    return AuthApi(host, schema)


@pytest.fixture(scope='session')
def ping_api(get_host, get_schema, logger_test):
    """Фикстура, создающая и возвращающая экземпляр api клиента Ping."""
    host = get_host
    schema = get_schema
    logger_test.info(
        f'Инициализация экземпляра АПИ клиента Ping: host {host}, '
        f'schema {schema}')
    return PingApi(host, schema)
