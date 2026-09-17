"""Тесты функций работы с пользователями."""

from users import add_user, find_user, sort_users


def test_add_user() -> None:
    users: dict[int, dict] = {}
    add_user(users, 'Михаил Хонинев')
    assert len(users) == 1
    assert users[1]['name'] == 'Михаил Хонинев'


def test_find_user() -> None:
    users: dict[int, dict] = {}
    add_user(users, 'Михаил Хонинев')
    add_user(users, 'Иван Иванов')
    found = find_user(users, 'хони')
    assert len(found) == 1
    assert found[0]['name'] == 'Михаил Хонинев'


def test_sort_users() -> None:
    users: dict[int, dict] = {}
    add_user(users, 'Михаил Хонинев')
    add_user(users, 'Анна Петрова')
    names = [item['name'] for item in sort_users(users)]
    assert names == ['Анна Петрова', 'Михаил Хонинев']
