"""Модуль с эндпоинтами для Booking."""


class Endpoints:
    """Эндпоинты."""

    GET_BOOKING_IDS = 'booking'
    GET_BOOKING = lambda self, uuid: f'booking/{uuid}'
    POST_BOOKING = 'booking'
    PUT_BOOKING = lambda self, uuid: f'booking/{uuid}'
    PATCH_BOOKING = lambda self, uuid: f'booking/{uuid}'
    DELETE_BOOKING = lambda self, uuid: f'booking/{uuid}'


class QueryParams:
    """Гет параметры."""

    FIRSTNAME = 'firstname'
    LASTNAME = 'lastname'
    CHECKIN = 'checkin'
    CHECKOUT = 'checkout'
