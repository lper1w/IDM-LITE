from vkbottle import API
from vkbottle.user import Message

from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.schemas.iris.methods import IrisDutyEventMethod


@route.method_handler(IrisDutyEventMethod.BAN_GET_REASON)
async def ban_get_reason(
    data: IrisDutyEvent,
    message: Message,
    api: API,
):
    message_data = await api.messages.get_by_conversation_message_id(
        peer_id=message.peer_id, conversation_message_ids=data.object.local_id
    )

    if not message_data.items:
        return {
            "response": "error",
            "error_code": 1,
            "error_message": "Сообщение с причиной бана не найдено.",
        }

    message_id = message_data.items[0].id
    await api.messages.send(
        peer_id=message.peer_id,
        message=f"🔥 Причина бана: {data.object.message or data.object.reason}",
        reply_to=message_id,
        random_id=0,
    )
