"""Тесты функций работы с API-ключами."""

from datetime import date

from entities.keys import (
    get_key_status,
    is_key_expired,
    is_key_usable,
    issue_key,
    mask_api_key,
    revoke_key,
)


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
    keys: dict[int, dict] = {}
    key = issue_key(keys, 1, 'write', date(2026, 12, 31))
    assert len(keys) == 1
    assert key['is_active'] is True
    revoke_key(keys, key['id'])
    assert keys[key['id']]['is_active'] is False


def test_duplicate_use_after_revoke_forbidden() -> None:
    keys: dict[int, dict] = {}
    key = issue_key(keys, 1, 'write', date(2026, 12, 31))
    today = date(2026, 9, 16)
    assert is_key_usable(keys, key['id'], today, 'write')
    revoke_key(keys, key['id'])
    assert not is_key_usable(keys, key['id'], today, 'write')
