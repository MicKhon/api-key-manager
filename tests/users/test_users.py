"""Тесты класса User и функций работы с пользователями."""

from entities.users import User, add_user, find_user, sort_users


def test_user_creation() -> None:
    user = User(1, 'Михаил Хонинев')
    assert user.id == 1
    assert user.name == 'Михаил Хонинев'
    assert str(user) == '1. Михаил Хонинев'


def test_user_from_data() -> None:
    user = User.from_data({'id': 2, 'name': 'Анна Петрова'})
    assert user.id == 2
    assert user.name == 'Анна Петрова'
    assert user.to_dict()['name'] == 'Анна Петрова'


def test_add_user() -> None:
    users: list[User] = []
    user = add_user(users, 'Михаил Хонинев')
    assert len(users) == 1
    assert users[0] is user
    assert user.name == 'Михаил Хонинев'


def test_find_user() -> None:
    users: list[User] = []
    add_user(users, 'Михаил Хонинев')
    add_user(users, 'Иван Иванов')
    found = find_user(users, 'хони')
    assert len(found) == 1
    assert found[0].name == 'Михаил Хонинев'


def test_sort_users() -> None:
    users: list[User] = []
    add_user(users, 'Михаил Хонинев')
    add_user(users, 'Анна Петрова')
    names = [item.name for item in sort_users(users)]
    assert names == ['Анна Петрова', 'Михаил Хонинев']
