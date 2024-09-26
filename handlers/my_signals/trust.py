from vkbottle import API
from vkbottle.user import Message

from app.config import settings
from app.core import route
from app.core.utils import IrisHandlerManager
from app.services.iris import IrisService


@route.my_signal_handler(commands=["+дов"])
async def add_trust(
    handler_manager: IrisHandlerManager,
    message: Message,
    api: API,
    service: IrisService,
):
    user_id = await handler_manager.search_user_id(message)
    user = service.get_user(id=settings.id)

    if user_id == message.from_id:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message="⚠️ Укажите пользователя.",
            keep_forward_messages=True,
        )
        return {"response": "ok"}

    if user_id in user.trust_users:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message=f"⚠️ Вы уже доверяете [id{user_id}|этому пользователю].",
            keep_forward_messages=True,
        )
        return {"response": "ok"}

    user.trust_users.append(user_id)

    service.update_user(user=user)
    await api.messages.edit(
        peer_id=message.peer_id,
        message_id=message.id,
        message=f"✅ Вы доверяете [id{user_id}|этому пользователю].",
        keep_forward_messages=True,
    )

    return {"response": "ok"}


@route.my_signal_handler(commands=["-дов"])
async def remove_trust(
    handler_manager: IrisHandlerManager,
    message: Message,
    api: API,
    service: IrisService,
):
    user_id = await handler_manager.search_user_id(message)
    user = service.get_user(id=settings.id)

    if user_id == message.from_id:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message="⚠️ Укажите пользователя.",
            keep_forward_messages=True,
        )
        return {"response": "ok"}

    if user_id not in user.trust_users:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message=f"⚠️ Вы не доверяете [id{user_id}|этому пользователю].",
            keep_forward_messages=True,
        )
        return {"response": "ok"}

    user.trust_users.remove(user_id)

    service.update_user(user=user)
    await api.messages.edit(
        peer_id=message.peer_id,
        message_id=message.id,
        message=f"✅ Вы больше не доверяете [id{user_id}|этому пользователю].",
        keep_forward_messages=True,
    )

    return {"response": "ok"}
