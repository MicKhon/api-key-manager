"""Тесты функций работы с разрешениями."""

from entities.permissions import (
    add_permission,
    find_permission,
    has_permission,
    sort_permissions,
)


def test_add_permission() -> None:
    permissions: dict[int, dict] = {}
    add_permission(permissions, 'write', 'Запись')
    assert len(permissions) == 1
    assert permissions[1]['code'] == 'write'


def test_find_permission() -> None:
    permissions: dict[int, dict] = {}
    add_permission(permissions, 'read', 'Чтение')
    add_permission(permissions, 'write', 'Запись')
    found = find_permission(permissions, 'WRITE')
    assert found is not None
    assert found['title'] == 'Запись'


def test_has_permission() -> None:
    assert has_permission('write', 'write')
    assert has_permission('admin', 'write')
    assert not has_permission('read', 'write')


def test_sort_permissions() -> None:
    permissions: dict[int, dict] = {}
    add_permission(permissions, 'write', 'Запись')
    add_permission(permissions, 'admin', 'Администратор')
    codes = [item['code'] for item in sort_permissions(permissions)]
    assert codes == ['admin', 'write']
