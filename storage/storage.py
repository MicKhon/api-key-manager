"""Сохранение и загрузка объектов проекта в JSON-файлах."""

import json
from pathlib import Path

from entities.applications.applications import (
    Application,
    find_application_by_id,
)
from entities.keys.keys import ApiKey
from entities.permissions.permissions import Permission, find_permission
from entities.users.users import User, find_user_by_id

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def _resolve(filename: str) -> Path:
    path = Path(filename)
    if path.is_absolute():
        return path
    return DATA_DIR / filename


def load_list(filename: str) -> list:
    """Загрузить список из JSON-файла.

    Если файла нет или JSON некорректен, возвращается пустой список.
    """
    path = _resolve(filename)
    try:
        with open(path, encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f'Файл {path} повреждён. Загружен пустой список.')
        return []
    if not isinstance(data, list):
        return []
    return data


def save_list(filename: str, items: list) -> None:
    """Сохранить список в JSON-файл через контекстный менеджер."""
    path = _resolve(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


def load_users(filename: str = 'users.json') -> list[User]:
    """Загрузить пользователей как объекты User."""
    items = load_list(filename)
    return [User.from_data(item) for item in items]


def save_users(
    users: list[User],
    filename: str = 'users.json',
) -> None:
    """Сохранить объекты User в JSON."""
    save_list(filename, [user.to_dict() for user in users])


def load_applications(
    users: list[User],
    filename: str = 'applications.json',
) -> list[Application]:
    """Загрузить приложения как объекты Application."""
    applications = []
    for item in load_list(filename):
        user = find_user_by_id(users, item['user_id'])
        if user is None:
            continue
        applications.append(Application.from_data(item, user))
    return applications


def save_applications(
    applications: list[Application],
    filename: str = 'applications.json',
) -> None:
    """Сохранить объекты Application в JSON."""
    save_list(
        filename,
        [application.to_dict() for application in applications],
    )


def load_permissions(
    filename: str = 'permissions.json',
) -> list[Permission]:
    """Загрузить разрешения как объекты Permission."""
    items = load_list(filename)
    return [Permission.from_data(item) for item in items]


def save_permissions(
    permissions: list[Permission],
    filename: str = 'permissions.json',
) -> None:
    """Сохранить объекты Permission в JSON."""
    save_list(
        filename,
        [permission.to_dict() for permission in permissions],
    )


def load_keys(
    applications: list[Application],
    permissions: list[Permission],
    filename: str = 'keys.json',
) -> list[ApiKey]:
    """Загрузить ключи как объекты ApiKey."""
    keys = []
    for item in load_list(filename):
        application = find_application_by_id(applications, item['app_id'])
        permission = find_permission(permissions, item['permission'])
        if application is None or permission is None:
            continue
        keys.append(ApiKey.from_data(item, application, permission))
    return keys


def save_keys(
    keys: list[ApiKey],
    filename: str = 'keys.json',
) -> None:
    """Сохранить объекты ApiKey в JSON."""
    save_list(filename, [key.to_dict() for key in keys])
