"""Класс разрешения и функции работы с коллекцией разрешений."""

from entities.base import Entity


class Permission(Entity):
    """Разрешение, которое можно выдать API-ключу."""

    def __init__(
        self,
        permission_id: int,
        code: str,
        title: str,
    ) -> None:
        """Создать объект разрешения."""
        super().__init__(permission_id)
        self.code = code
        self.title = title

    @classmethod
    def from_data(cls, data: dict) -> 'Permission':
        """Создать разрешение из словаря JSON."""
        return cls(
            permission_id=data['id'],
            code=data['code'],
            title=data['title'],
        )

    @staticmethod
    def validate_code(code: str) -> bool:
        """Проверить, что код разрешения известен системе."""
        return code in {'read', 'write', 'admin'}

    def covers(self, required_permission: str) -> bool:
        """Проверить, достаточно ли этого разрешения для действия."""
        if self.code == 'admin':
            return True
        return self.code == required_permission

    def to_dict(self) -> dict:
        """Преобразовать разрешение в данные JSON."""
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление разрешения."""
        return f'{self.id}. {self.code} — {self.title}'


def _next_id(permissions: list[Permission]) -> int:
    """Вернуть следующий идентификатор для коллекции."""
    if not permissions:
        return 1
    return max(permission.id for permission in permissions) + 1


def add_permission(
    permissions: list[Permission],
    code: str,
    title: str,
) -> Permission:
    """Создать объект Permission и добавить его в коллекцию."""
    permission = Permission(_next_id(permissions), code, title)
    permissions.append(permission)
    return permission


def find_permission(
    permissions: list[Permission],
    code: str,
) -> Permission | None:
    """Найти разрешение по коду или вернуть None."""
    needle = code.lower()
    for permission in permissions:
        if permission.code.lower() == needle:
            return permission
    return None


def find_permission_by_id(
    permissions: list[Permission],
    permission_id: int,
) -> Permission | None:
    """Вернуть разрешение по идентификатору или None."""
    for permission in permissions:
        if permission.id == permission_id:
            return permission
    return None


def sort_permissions(
    permissions: list[Permission],
) -> list[Permission]:
    """Вернуть разрешения, отсортированные по коду."""
    return sorted(
        permissions,
        key=lambda item: item.code.lower(),
    )


def has_permission(
    user_permission: str,
    required_permission: str,
) -> bool:
    """Проверить достаточность строкового кода разрешения."""
    if user_permission == 'admin':
        return True
    if user_permission == required_permission:
        return True
    return False
