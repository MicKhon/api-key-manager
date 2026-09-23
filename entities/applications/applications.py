"""Класс приложения и функции работы с коллекцией приложений."""

from entities.base import Entity
from entities.users.users import User


class Application(Entity):
    """Приложение, принадлежащее пользователю."""

    def __init__(
        self,
        application_id: int,
        name: str,
        user: User,
    ) -> None:
        """Создать объект приложения."""
        super().__init__(application_id)
        self.name = name
        self.user = user

    @classmethod
    def from_data(cls, data: dict, user: User) -> 'Application':
        """Создать приложение из словаря JSON и объекта User."""
        return cls(
            application_id=data['id'],
            name=data['name'],
            user=user,
        )

    def belongs_to(self, user_id: int) -> bool:
        """Проверить, принадлежит ли приложение пользователю."""
        return self.user.id == user_id

    def to_dict(self) -> dict:
        """Преобразовать приложение в данные JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user.id,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление приложения."""
        return f'{self.id}. {self.name} ({self.user.name})'


def _next_id(applications: list[Application]) -> int:
    """Вернуть следующий идентификатор для коллекции."""
    if not applications:
        return 1
    return max(application.id for application in applications) + 1


def add_application(
    applications: list[Application],
    name: str,
    user: User,
) -> Application:
    """Создать объект Application и добавить его в коллекцию."""
    application = Application(_next_id(applications), name, user)
    applications.append(application)
    return application


def find_application(
    applications: list[Application],
    query: str,
) -> list[Application]:
    """Найти приложения по подстроке названия без учёта регистра."""
    needle = query.lower()
    found = []
    for application in applications:
        if needle in application.name.lower():
            found.append(application)
    return found


def find_application_by_id(
    applications: list[Application],
    application_id: int,
) -> Application | None:
    """Вернуть приложение по идентификатору или None."""
    for application in applications:
        if application.id == application_id:
            return application
    return None


def filter_applications_by_user(
    applications: list[Application],
    user_id: int,
):
    """Отобрать приложения пользователя. Возвращает генератор."""
    return (
        application
        for application in applications
        if application.belongs_to(user_id)
    )


def sort_applications(
    applications: list[Application],
) -> list[Application]:
    """Вернуть приложения, отсортированные по названию."""
    return sorted(
        applications,
        key=lambda item: item.name.lower(),
    )
