from typing import Generic, TypeVar

from pydantic import BaseModel

from .methods import IrisDutyEventMethod
from .models import IrisDutyEventMessage, IrisDutyEventObject

T = TypeVar("T", bound=BaseModel)


class IrisDutyEvent(BaseModel, Generic[T]):
    """Основная модель события, включающая метод и объект события."""

    user_id: int
    method: IrisDutyEventMethod
    secret: str
    message: IrisDutyEventMessage | None
    object: IrisDutyEventObject | T | None
