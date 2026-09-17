"""Тесты функций работы с приложениями."""

from applications import (
    add_application,
    filter_applications_by_user,
    find_application,
    sort_applications,
)


def test_add_application() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Платежный шлюз', 1)
    assert len(applications) == 1
    assert applications[1]['name'] == 'Платежный шлюз'
    assert applications[1]['user_id'] == 1


def test_find_application() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Платежный шлюз', 1)
    add_application(applications, 'Мобильный клиент', 1)
    found = find_application(applications, 'платеж')
    assert len(found) == 1
    assert found[0]['name'] == 'Платежный шлюз'


def test_sort_applications() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Мобильный клиент', 1)
    add_application(applications, 'Платежный шлюз', 1)
    names = [item['name'] for item in sort_applications(applications)]
    assert names == ['Мобильный клиент', 'Платежный шлюз']


def test_filter_applications_by_user() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Платежный шлюз', 1)
    add_application(applications, 'Другое приложение', 2)
    owned = list(filter_applications_by_user(applications, 1))
    assert len(owned) == 1
    assert owned[0]['name'] == 'Платежный шлюз'
