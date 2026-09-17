"""Функции для работы с разрешениями."""


def add_permission(
    permissions: dict[int, dict],
    code: str,
    title: str,
) -> None:
    """Добавить разрешение в словарь permissions."""
    next_id = max(permissions, default=0) + 1
    permissions[next_id] = {
        'id': next_id,
        'code': code,
        'title': title,
    }


def find_permission(
    permissions: dict[int, dict],
    code: str,
) -> dict | None:
    """Найти разрешение по коду или вернуть None."""
    needle = code.lower()
    for permission in permissions.values():
        if permission['code'].lower() == needle:
            return permission
    return None


def sort_permissions(permissions: dict[int, dict]) -> list[dict]:
    """Вернуть разрешения, отсортированные по коду."""
    return sorted(
        permissions.values(),
        key=lambda item: item['code'].lower(),
    )


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
