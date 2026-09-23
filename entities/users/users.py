"""Класс пользователя и функции работы с коллекцией пользователей."""

from entities.base import Entity


class User(Entity):
    """Пользователь сервиса управления API-ключами."""

    def __init__(self, user_id: int, name: str) -> None:
        """Создать объект пользователя."""
        super().__init__(user_id)
        self.name = name

    @classmethod
    def from_data(cls, data: dict) -> 'User':
        """Создать пользователя из словаря JSON."""
        return cls(
            user_id=data['id'],
            name=data['name'],
        )

    def to_dict(self) -> dict:
        """Преобразовать пользователя в данные JSON."""
        return {
            'id': self.id,
            'name': self.name,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f'{self.id}. {self.name}'


def _next_id(users: list[User]) -> int:
    """Вернуть следующий идентификатор для коллекции."""
    if not users:
        return 1
    return max(user.id for user in users) + 1


def add_user(users: list[User], name: str) -> User:
    """Создать объект User и добавить его в коллекцию."""
    user = User(_next_id(users), name)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке имени."""
    needle = query.lower()
    found = []
    for user in users:
        if needle in user.name.lower():
            found.append(user)
    return found


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Вернуть пользователя по идентификатору или None."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def sort_users(users: list[User]) -> list[User]:
    """Вернуть пользователей, отсортированных по имени."""
    return sorted(users, key=lambda item: item.name.lower())
