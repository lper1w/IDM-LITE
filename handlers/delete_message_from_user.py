from datetime import datetime

from vkbottle import API, VKAPIError
from vkbottle.user import Message

from app.core import route
from app.core.utils import IrisHandlerManager
from app.schemas.iris.event import IrisDutyEvent
from app.schemas.iris.methods import IrisDutyEventMethod


@route.method_handler(method=IrisDutyEventMethod.DELETE_MESSAGES_FROM_USER)
async def delete_message_from_user(
    handler_manager: IrisHandlerManager,
    data: IrisDutyEvent,
    message: Message,
    api: API,
):
    message_id = await api.messages.send(
        peer_id=message.peer_id,
        message=f"🔥 {message.from_id} удаление сообщеня от @id{data.object.user_id} из чата.",
        random_id=0,
    )

    cmids = []
    amount = data.object.amount

    async for message in handler_manager.get_all_history(message.peer_id):
        if datetime.now().timestamp() - message.date >= 86400:
            break

        if message.from_id == data.object.user_id and message.action is None:
            cmids.append(str(message.conversation_message_id))

    if amount and amount <= len(cmids):
        cmids = cmids[: len(cmids) - (len(cmids) - amount)]

    try:
        await api.messages.delete(
            peer_id=message.peer_id,
            cmids=cmids,
            delete_for_all=True,
            spam=True if data.object.is_spam else False,
        )

        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message_id,
            message=f"✅ @id{message.from_id} удаление сообщеня от @id{data.object.user_id} из чата. Сообщений удалено: {len(cmids)}.",
        )
    except VKAPIError as e:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message_id,
            message=f"❗ @id{message.from_id} удаление сообщеня от @id{data.object.user_id} из чата. Ошибка: {e.error_msg}",
        )
    except Exception:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message_id,
            message=f"❗ @id{message.from_id} удаление сообщеня от @id{data.object.user_id} из чата. Неизвестная ошибка.",
        )

    finally:
        return {"response": "ok"}
        return {"response": "ok"}
