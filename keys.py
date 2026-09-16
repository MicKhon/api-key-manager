"""Функции для работы с API-ключами."""

from datetime import date

from utils import generate_key_value


def get_key_status(is_active: bool) -> str:
    """Возвращает текстовый статус API-ключа."""
    if is_active:
        return 'Ключ активен'
    return 'Ключ отозван'


def is_key_expired(expiry_date: date, today: date) -> bool:
    """Проверяет, истёк ли срок действия ключа."""
    if expiry_date < today:
        return True
    return False


def has_permission(
    user_permission: str,
    required_permission: str,
) -> bool:
    """Проверяет, достаточно ли разрешения для действия."""
    if user_permission == 'admin':
        return True
    if user_permission == required_permission:
        return True
    return False


def mask_api_key(api_key: str) -> str:
    """Маскирует ключ, оставляя видимыми крайние символы."""
    if len(api_key) < 8:
        return '***'
    prefix = api_key[0:4]
    suffix = api_key[-4:]
    return prefix + '...' + suffix


def _as_date(value: date | str) -> date:
    """Преобразовать строку ISO или объект date к date."""
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def issue_key(
    keys: dict[int, dict],
    app_id: int,
    permission: str,
    expiry_date: date,
) -> dict:
    """Выпустить новый API-ключ для приложения."""
    next_id = max(keys, default=0) + 1
    key = {
        'id': next_id,
        'app_id': app_id,
        'value': generate_key_value(),
        'is_active': True,
        'permission': permission,
        'expiry_date': expiry_date.isoformat(),
    }
    keys[next_id] = key
    return key


def revoke_key(keys: dict[int, dict], key_id: int) -> None:
    """Отозвать ключ по идентификатору."""
    if key_id not in keys:
        raise ValueError('Ключ не найден')
    keys[key_id]['is_active'] = False


def find_key(keys: dict[int, dict], key_id: int) -> dict | None:
    """Вернуть ключ по идентификатору или None."""
    return keys.get(key_id)


def is_key_usable(
    keys: dict[int, dict],
    key_id: int,
    today: date,
    required_permission: str,
) -> bool:
    """Проверить, можно ли использовать ключ для действия."""
    key = find_key(keys, key_id)
    if key is None:
        return False
    if not key['is_active']:
        return False
    expiry_date = _as_date(key['expiry_date'])
    if is_key_expired(expiry_date, today):
        return False
    return has_permission(key['permission'], required_permission)


def filter_active_keys(keys: dict[int, dict]):
    """Вернуть генератор активных ключей."""
    return (key for key in keys.values() if key['is_active'])


def sort_keys(keys: dict[int, dict]) -> list[dict]:
    """Вернуть ключи, отсортированные по дате окончания срока."""
    return sorted(
        keys.values(),
        key=lambda item: item['expiry_date'],
    )


def get_keys_stats(keys: dict[int, dict]) -> dict[str, int]:
    """Посчитать статистику по ключам."""
    active_count = 0
    revoked_count = 0
    for key in keys.values():
        if key['is_active']:
            active_count += 1
        else:
            revoked_count += 1
    return {
        'total': len(keys),
        'active': active_count,
        'revoked': revoked_count,
    }
