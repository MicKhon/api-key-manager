"""Разрешение."""

from entities.permissions.permissions import (
    Permission,
    add_permission,
    find_permission,
    find_permission_by_id,
    has_permission,
    sort_permissions,
)

__all__ = [
    'Permission',
    'add_permission',
    'find_permission',
    'find_permission_by_id',
    'has_permission',
    'sort_permissions',
]
