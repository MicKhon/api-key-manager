"""Тесты класса Permission и функций работы с разрешениями."""

from entities.permissions import (
    Permission,
    add_permission,
    find_permission,
    has_permission,
    sort_permissions,
)


def test_permission_creation() -> None:
    permission = Permission(2, 'write', 'Запись')
    assert permission.id == 2
    assert permission.code == 'write'
    assert permission.title == 'Запись'
    assert permission.covers('write')
    assert not permission.covers('admin')
    assert 'write' in str(permission)


def test_permission_from_data() -> None:
    permission = Permission.from_data(
        {'id': 3, 'code': 'admin', 'title': 'Администратор'},
    )
    assert permission.covers('write')
    assert Permission.validate_code('read')
    assert not Permission.validate_code('delete')


def test_add_permission() -> None:
    permissions: list[Permission] = []
    permission = add_permission(permissions, 'write', 'Запись')
    assert len(permissions) == 1
    assert permissions[0] is permission
    assert permission.code == 'write'


def test_find_permission() -> None:
    permissions: list[Permission] = []
    add_permission(permissions, 'read', 'Чтение')
    add_permission(permissions, 'write', 'Запись')
    found = find_permission(permissions, 'WRITE')
    assert found is not None
    assert found.title == 'Запись'


def test_has_permission() -> None:
    assert has_permission('write', 'write')
    assert has_permission('admin', 'write')
    assert not has_permission('read', 'write')


def test_sort_permissions() -> None:
    permissions: list[Permission] = []
    add_permission(permissions, 'write', 'Запись')
    add_permission(permissions, 'admin', 'Администратор')
    codes = [item.code for item in sort_permissions(permissions)]
    assert codes == ['admin', 'write']
