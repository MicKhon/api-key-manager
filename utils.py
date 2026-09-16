"""Вспомогательные функции ввода и генерации ключа."""

import secrets
from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        raw_value = input(prompt).strip()
        try:
            return int(raw_value)
        except ValueError:
            print('Нужно целое число. Повторите ввод.')


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        raw_value = input(prompt).strip()
        try:
            return datetime.strptime(raw_value, '%Y-%m-%d').date()
        except ValueError:
            print('Некорректная дата. Используйте формат ГГГГ-ММ-ДД.')


def generate_key_value() -> str:
    """Сгенерировать значение API-ключа."""
    return 'ak_live_' + secrets.token_hex(6)
