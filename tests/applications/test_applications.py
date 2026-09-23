"""Тесты класса Application и функций работы с приложениями."""

from entities.applications import (
    Application,
    add_application,
    filter_applications_by_user,
    find_application,
    sort_applications,
)
from entities.users import User


def _owner() -> User:
    return User(1, 'Михаил Хонинев')


def test_application_creation() -> None:
    user = _owner()
    application = Application(1, 'Платежный шлюз', user)
    assert application.id == 1
    assert application.name == 'Платежный шлюз'
    assert application.user is user
    assert application.belongs_to(1)
    assert 'Платежный шлюз' in str(application)


def test_add_application() -> None:
    applications: list[Application] = []
    user = _owner()
    application = add_application(applications, 'Платежный шлюз', user)
    assert len(applications) == 1
    assert applications[0] is application
    assert application.user.id == 1


def test_find_application() -> None:
    applications: list[Application] = []
    user = _owner()
    add_application(applications, 'Платежный шлюз', user)
    add_application(applications, 'Мобильный клиент', user)
    found = find_application(applications, 'платеж')
    assert len(found) == 1
    assert found[0].name == 'Платежный шлюз'


def test_sort_applications() -> None:
    applications: list[Application] = []
    user = _owner()
    add_application(applications, 'Мобильный клиент', user)
    add_application(applications, 'Платежный шлюз', user)
    names = [item.name for item in sort_applications(applications)]
    assert names == ['Мобильный клиент', 'Платежный шлюз']


def test_filter_applications_by_user() -> None:
    applications: list[Application] = []
    owner = _owner()
    other = User(2, 'Иван Иванов')
    add_application(applications, 'Платежный шлюз', owner)
    add_application(applications, 'Другое приложение', other)
    owned = list(filter_applications_by_user(applications, 1))
    assert len(owned) == 1
    assert owned[0].name == 'Платежный шлюз'
