"""Тесты класса ApiKey и функций работы с API-ключами."""

from datetime import date

from entities.applications import Application
from entities.keys import (
    ApiKey,
    get_key_status,
    is_key_expired,
    is_key_usable,
    issue_key,
    mask_api_key,
    revoke_key,
)
from entities.permissions import Permission
from entities.users import User


def _application() -> Application:
    user = User(1, 'Михаил Хонинев')
    return Application(1, 'Платежный шлюз', user)


def _permission(code: str = 'write') -> Permission:
    titles = {
        'read': 'Чтение',
        'write': 'Запись',
        'admin': 'Администратор',
    }
    return Permission(1, code, titles[code])


def test_api_key_creation() -> None:
    application = _application()
    permission = _permission()
    key = ApiKey(
        1,
        application,
        'ak_live_9f3a2c1b8e7d',
        True,
        permission,
        date(2026, 12, 31),
    )
    assert key.id == 1
    assert key.application is application
    assert key.permission is permission
    assert key.status == 'Ключ активен'
    assert 'Платежный шлюз' in str(key)


def test_get_key_status() -> None:
    assert get_key_status(True) == 'Ключ активен'
    assert get_key_status(False) == 'Ключ отозван'


def test_is_key_expired() -> None:
    today = date(2026, 9, 16)
    assert is_key_expired(date(2026, 1, 1), today)
    assert not is_key_expired(date(2026, 12, 31), today)


def test_mask_api_key() -> None:
    assert mask_api_key('ak_live_9f3a2c1b8e7d') == 'ak_l...8e7d'


def test_issue_and_revoke_key() -> None:
    keys: list[ApiKey] = []
    key = issue_key(
        keys,
        _application(),
        _permission(),
        date(2026, 12, 31),
    )
    assert len(keys) == 1
    assert key.is_active is True
    revoke_key(keys, key.id)
    assert key.is_active is False
    assert key.status == 'Ключ отозван'


def test_duplicate_use_after_revoke_forbidden() -> None:
    keys: list[ApiKey] = []
    key = issue_key(
        keys,
        _application(),
        _permission(),
        date(2026, 12, 31),
    )
    today = date(2026, 9, 16)
    assert is_key_usable(keys, key.id, today, 'write')
    revoke_key(keys, key.id)
    assert not is_key_usable(keys, key.id, today, 'write')


def test_key_interaction_with_application() -> None:
    application = _application()
    permission = _permission('admin')
    key = ApiKey(
        1,
        application,
        'ak_live_9f3a2c1b8e7d',
        True,
        permission,
        date(2026, 12, 31),
    )
    assert key.application.user.name == 'Михаил Хонинев'
    assert key.is_usable(date(2026, 9, 16), 'write')
