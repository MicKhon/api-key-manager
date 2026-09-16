"""Функции для работы с приложениями."""


def add_application(
    applications: dict[int, dict],
    name: str,
    owner: str,
) -> None:
    """Добавить приложение в словарь applications."""
    next_id = max(applications, default=0) + 1
    applications[next_id] = {
        'id': next_id,
        'name': name,
        'owner': owner,
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


def filter_applications_by_owner(
    applications: dict[int, dict],
    owner: str,
):
    """Отобрать приложения владельца. Возвращает генератор."""
    owner_lower = owner.lower()
    return (
        application
        for application in applications.values()
        if application['owner'].lower() == owner_lower
    )


def sort_applications(applications: dict[int, dict]) -> list[dict]:
    """Вернуть приложения, отсортированные по названию."""
    return sorted(
        applications.values(),
        key=lambda item: item['name'].lower(),
    )
