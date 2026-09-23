"""Базовый класс сущностей предметной области."""


class Entity:
    """Сущность с идентификатором.

    От этого класса наследуют User, Application, Permission и ApiKey.
    """

    def __init__(self, entity_id: int) -> None:
        """Сохранить идентификатор объекта."""
        self.id = entity_id

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        raise NotImplementedError
