"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / 'data'


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


def load_applications(
    filename: str = 'applications.json',
) -> dict[int, dict]:
    """Загрузить приложения и вернуть словарь по идентификатору."""
    items = load_list(filename)
    return {item['id']: item for item in items}


def save_applications(
    applications: dict[int, dict],
    filename: str = 'applications.json',
) -> None:
    """Сохранить приложения в JSON-файл."""
    save_list(filename, list(applications.values()))


def load_keys(filename: str = 'keys.json') -> dict[int, dict]:
    """Загрузить ключи и вернуть словарь по идентификатору."""
    items = load_list(filename)
    return {item['id']: item for item in items}


def save_keys(
    keys: dict[int, dict],
    filename: str = 'keys.json',
) -> None:
    """Сохранить ключи в JSON-файл."""
    save_list(filename, list(keys.values()))
