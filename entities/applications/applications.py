"""Функции для работы с приложениями."""


def add_application(
    applications: dict[int, dict],
    name: str,
    user_id: int,
) -> None:
    """Добавить приложение в словарь applications."""
    next_id = max(applications, default=0) + 1
    applications[next_id] = {
        'id': next_id,
        'name': name,
        'user_id': user_id,
    }


def find_application(
    applications: dict[int, dict],
    query: str,
) -> list[dict]:
    """Найти приложения по подстроке названия без учёта регистра."""
    needle = query.lower()
    found = []
    for application in applications.values():
        if needle in application['name'].lower():
            found.append(application)
    return found


def filter_applications_by_user(
    applications: dict[int, dict],
    user_id: int,
):
    """Отобрать приложения пользователя. Возвращает генератор."""
    return (
        application
        for application in applications.values()
        if application['user_id'] == user_id
    )


def sort_applications(applications: dict[int, dict]) -> list[dict]:
    """Вернуть приложения, отсортированные по названию."""
    return sorted(
        applications.values(),
        key=lambda item: item['name'].lower(),
    )
