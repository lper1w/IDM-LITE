from inspect import Parameter, Signature
from typing import Any, Dict, Optional, Type, TypeVar

from loguru import logger

from .base import BaseModel
from .fields import Field
from .storage import JsonStorage

T = TypeVar("T", bound="BaseModelMeta")


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {name: attr for name, attr in attrs.items() if isinstance(attr, Field)}
        attrs["_meta"] = {"model_name": name.lower(), "fields": fields}

        def create(cls, **kwargs):
            instance = cls(**kwargs)
            if "id" not in kwargs:
                logger.error(f"Missing 'id' for instance creation in '{cls.__name__}'")
                raise ValueError("Field 'id' is required")
            cls.save(instance)
            return instance

        params = {
            field_name: Parameter(
                field_name,
                Parameter.POSITIONAL_OR_KEYWORD,
                annotation=field_type.field_type,
            )
            for field_name, field_type in fields.items()
        }

        create.__signature__ = Signature(
            parameters=params.values(),
            return_annotation=cls,
        )

        attrs["create"] = classmethod(create)
        return super().__new__(cls, name, bases, attrs)


class BaseModelMeta(BaseModel, metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for field_name, field_instance in self._meta["fields"].items():
            setattr(self, field_name, kwargs.get(field_name))
        for field_name in self._meta["fields"].keys():
            if getattr(self, field_name, None) is None:
                logger.warning(f"Field '{field_name}' not set during initialization.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта в словарь. Подсказки типов вернутся для этого метода.
        :return словарь
        """
        return {
            field_name: getattr(self, field_name) for field_name in self._meta["fields"]
        }

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Создание экземпляра модели из словаря данных.
        :return: экземпляр модели
        """
        return cls(**data)

    @classmethod
    def get(cls: Type[T], id: int) -> Optional[T]:
        """
        Получение экземпляра модели по id.
        :return: экземпляр или None
        """
        data = JsonStorage.get(cls._meta["model_name"], id)
        if data:
            return cls.from_dict(data)
        return None

    @classmethod
    def save(cls: Type[T], instance: T) -> None:
        """
        Сохранение экземпляра модели.
        """
        if not hasattr(instance, "id"):
            logger.error(f"Instance of '{cls.__name__}' has no attribute 'id'")
            raise AttributeError(f"Instance of '{cls.__name__}' has no attribute 'id'")
        JsonStorage.save(
            cls._meta["model_name"], getattr(instance, "id"), instance.to_dict()
        )

    @classmethod
    def delete(cls, id: int) -> None:
        """
        Удаление экземпляра модели по id.
        """
        JsonStorage.delete(cls._meta["model_name"], id)

    @classmethod
    def all(cls: Type[T]) -> Dict[int, T]:
        """
        Возвращает все экземпляры модели.
        :return: словарь с экземплярами
        """
        return [
            cls.from_dict(item) for item in JsonStorage.all(cls._meta["model_name"])
        ]

    @classmethod
    def create(cls, **kwargs):
        """
        Создать и сохранить новый экземпляр модели.
        :param kwargs: параметры для создания экземпляра
        :return: созданный экземпляр
        """
        instance = cls(**kwargs)
        cls.save(instance)
        return instance

    @classmethod
    def update(cls, id: int, **kwargs) -> Optional[T]:
        """
        Обновить экземпляр модели по id.
        :param id: идентификатор экземпляра для обновления
        :param kwargs: новые значения для полей
        :return: обновленный экземпляр или None, если экземпляр не найден
        """
        model = cls.get(id)

        if model is None:
            logger.warning(f"Экземпляр с id {id} не найден для обновления.")
            return None

        for field_name, value in kwargs.items():
            if field_name in cls._meta["fields"]:
                setattr(model, field_name, value)
            else:
                logger.warning(
                    f"Поле '{field_name}' не существует в модели '{cls.__name__}'."
                )

        cls.save(model)
        return model
