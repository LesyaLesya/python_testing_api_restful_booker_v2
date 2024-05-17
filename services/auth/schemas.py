"""Модуль со схемами."""

from pydantic import BaseModel


class AuthTokenSchema(BaseModel):
    token: str
