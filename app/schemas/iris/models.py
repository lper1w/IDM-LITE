from datetime import datetime

from pydantic import BaseModel, Field


class IrisDutyEventMessage(BaseModel):
    """Модель сообщения события."""

    conversation_message_id: int
    from_id: int
    date: datetime
    text: str


class IrisDutyEventObject(BaseModel):
    """Данные для конкретных методов."""

    from_id: int | None = Field(default=None)
    chat: str | None = Field(default=None)
    text: str | None = Field(default=None)
    conversation_message_id: int | None = Field(default=None)
    is_spam: bool | None = Field(default=None)
    silent: bool | None = Field(default=None)
    user_id: int | None = Field(default=None)
    member_ids: list[int] | None = Field(default=None)
    reason: str | None = Field(default=None)
    message: str | None = Field(default=None)
    source: str | None = Field(default=None)
    amount: int | None = Field(default=None)
    local_id: int | None = Field(default=None)
    local_ids: list[int] | None = Field(default=None)
    description: str | None = Field(default=None)
    value: str | None = Field(default=None)
    price: int | None = Field(default=None)
    group_id: int | None = Field(default=None)
