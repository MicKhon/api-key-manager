"""Класс API-ключа и функции работы с коллекцией ключей."""

from datetime import date

from entities.applications.applications import Application
from entities.base import Entity
from entities.permissions.permissions import Permission
from utils.utils import generate_key_value


class ApiKey(Entity):
    """API-ключ, выпущенный для приложения."""

    def __init__(
        self,
        key_id: int,
        application: Application,
        value: str,
        is_active: bool,
        permission: Permission,
        expiry_date: date,
    ) -> None:
        """Создать объект API-ключа."""
        super().__init__(key_id)
        self.application = application
        self.value = value
        self.is_active = is_active
        self.permission = permission
        self.expiry_date = expiry_date

    @classmethod
    def from_data(
        cls,
        data: dict,
        application: Application,
        permission: Permission,
    ) -> 'ApiKey':
        """Создать ключ из словаря JSON и связанных объектов."""
        return cls(
            key_id=data['id'],
            application=application,
            value=data['value'],
            is_active=data['is_active'],
            permission=permission,
            expiry_date=date.fromisoformat(data['expiry_date']),
        )

    @staticmethod
    def mask_value(api_key: str) -> str:
        """Маскировать ключ, оставляя видимыми крайние символы."""
        if len(api_key) < 8:
            return '***'
        prefix = api_key[0:4]
        suffix = api_key[-4:]
        return prefix + '...' + suffix

    @staticmethod
    def is_expired(expiry_date: date, today: date) -> bool:
        """Проверить, истёк ли срок действия ключа."""
        return expiry_date < today

    @property
    def status(self) -> str:
        """Вернуть текстовый статус ключа."""
        if self.is_active:
            return 'Ключ активен'
        return 'Ключ отозван'

    def revoke(self) -> None:
        """Отозвать ключ, изменив его состояние."""
        self.is_active = False

    def is_usable(self, today: date, required_permission: str) -> bool:
        """Проверить, можно ли использовать ключ для действия."""
        if not self.is_active:
            return False
        if self.is_expired(self.expiry_date, today):
            return False
        return self.permission.covers(required_permission)

    def to_dict(self) -> dict:
        """Преобразовать ключ в данные JSON."""
        return {
            'id': self.id,
            'app_id': self.application.id,
            'value': self.value,
            'is_active': self.is_active,
            'permission': self.permission.code,
            'expiry_date': self.expiry_date.isoformat(),
        }

    def __str__(self) -> str:
        """Вернуть строковое представление ключа."""
        masked = self.mask_value(self.value)
        return (
            f'{self.id}. {self.application.name} '
            f'{masked} ({self.status})'
        )


def _next_id(keys: list[ApiKey]) -> int:
    """Вернуть следующий идентификатор для коллекции."""
    if not keys:
        return 1
    return max(key.id for key in keys) + 1


def get_key_status(is_active: bool) -> str:
    """Вернуть текстовый статус по признаку активности."""
    if is_active:
        return 'Ключ активен'
    return 'Ключ отозван'


def is_key_expired(expiry_date: date, today: date) -> bool:
    """Проверить, истёк ли срок действия ключа."""
    return ApiKey.is_expired(expiry_date, today)


def mask_api_key(api_key: str) -> str:
    """Маскировать значение ключа."""
    return ApiKey.mask_value(api_key)


def issue_key(
    keys: list[ApiKey],
    application: Application,
    permission: Permission,
    expiry_date: date,
) -> ApiKey:
    """Выпустить новый API-ключ для приложения."""
    key = ApiKey(
        key_id=_next_id(keys),
        application=application,
        value=generate_key_value(),
        is_active=True,
        permission=permission,
        expiry_date=expiry_date,
    )
    keys.append(key)
    return key


def find_key(keys: list[ApiKey], key_id: int) -> ApiKey | None:
    """Вернуть ключ по идентификатору или None."""
    for key in keys:
        if key.id == key_id:
            return key
    return None


def revoke_key(keys: list[ApiKey], key_id: int) -> None:
    """Отозвать ключ по идентификатору."""
    key = find_key(keys, key_id)
    if key is None:
        raise ValueError('Ключ не найден')
    key.revoke()


def is_key_usable(
    keys: list[ApiKey],
    key_id: int,
    today: date,
    required_permission: str,
) -> bool:
    """Проверить, можно ли использовать ключ для действия."""
    key = find_key(keys, key_id)
    if key is None:
        return False
    return key.is_usable(today, required_permission)


def filter_active_keys(keys: list[ApiKey]):
    """Вернуть генератор активных ключей."""
    return (key for key in keys if key.is_active)


def sort_keys(keys: list[ApiKey]) -> list[ApiKey]:
    """Вернуть ключи, отсортированные по дате окончания срока."""
    return sorted(keys, key=lambda item: item.expiry_date)


def get_keys_stats(keys: list[ApiKey]) -> dict[str, int]:
    """Посчитать статистику по ключам."""
    active_count = 0
    revoked_count = 0
    for key in keys:
        if key.is_active:
            active_count += 1
        else:
            revoked_count += 1
    return {
        'total': len(keys),
        'active': active_count,
        'revoked': revoked_count,
    }
