"""Функции для работы с пользователями."""


def add_user(users: dict[int, dict], name: str) -> None:
    """Добавить пользователя в словарь users."""
    next_id = max(users, default=0) + 1
    users[next_id] = {
        'id': next_id,
        'name': name,
    }


def find_user(users: dict[int, dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке имени."""
    needle = query.lower()
    found = []
    for user in users.values():
        if needle in user['name'].lower():
            found.append(user)
    return found


def sort_users(users: dict[int, dict]) -> list[dict]:
    """Вернуть пользователей, отсортированных по имени."""
    return sorted(
        users.values(),
        key=lambda item: item['name'].lower(),
    )
