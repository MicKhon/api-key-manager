"""Тесты функций работы с приложениями."""

from applications import (
    add_application,
    filter_applications_by_owner,
    find_application,
    sort_applications,
)


def test_add_application() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Платежный шлюз', 'Михаил Хонинев')
    assert len(applications) == 1
    assert applications[1]['name'] == 'Платежный шлюз'


def test_find_application() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Платежный шлюз', 'Михаил Хонинев')
    add_application(applications, 'Мобильный клиент', 'Михаил Хонинев')
    found = find_application(applications, 'платеж')
    assert len(found) == 1
    assert found[0]['name'] == 'Платежный шлюз'


def test_sort_applications() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Мобильный клиент', 'Михаил Хонинев')
    add_application(applications, 'Платежный шлюз', 'Михаил Хонинев')
    names = [item['name'] for item in sort_applications(applications)]
    assert names == ['Мобильный клиент', 'Платежный шлюз']


def test_filter_applications_by_owner() -> None:
    applications: dict[int, dict] = {}
    add_application(applications, 'Платежный шлюз', 'Михаил Хонинев')
    add_application(applications, 'Другое приложение', 'Иван Иванов')
    owned = list(
        filter_applications_by_owner(applications, 'Михаил Хонинев')
    )
    assert len(owned) == 1
    assert owned[0]['name'] == 'Платежный шлюз'
