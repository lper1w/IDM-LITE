from loguru import logger
from vkbottle import API
from vkbottle.user import Message

from app.config import settings
from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.schemas.iris.methods import IrisDutyEventMethod
from app.services.iris import IrisService


@route.method_handler(method=IrisDutyEventMethod.SUBSCRIBE_SIGNALS)
async def subscribe_signals(
    data: IrisDutyEvent,
    message: Message,
    api: API,
    service: IrisService,
):
    chats = service.get_chats(id=settings.id)

    for chat in chats:
        if chat["id"] != data.object.chat:
            continue

        chat["installed"] = True
        logger.info(f"Чат с id '{data.object.chat}' найден и обновлен: {chat}")
        break

    user = service.get_user(id=settings.id)
    user.chats = chats

    service.update_user(user=user)

    edit_message = f"""
    🔥 Успешно. Я подписался на сигналы.
    🎊 Iris chat id: {data.object.chat}
    🗨️ Peer id: {message.peer_id}
    """

    await api.messages.edit(
        peer_id=message.peer_id,
        message_id=message.id,
        message=edit_message,
    )

    return {"response": "ok"}
