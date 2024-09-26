from vkbottle import API
from vkbottle.user import Message

from app.config import settings
from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.services.iris import IrisService


@route.my_signal_handler(commands=["инфо"])
async def get_user_info(
    api: API, data: IrisDutyEvent, message: Message, service: IrisService
):
    user = service.get_user(id=settings.id)

    api_user_data = await api.users.get(user_ids=user.id)
    chat = await api.messages.get_chat(chat_id=message.peer_id - 2000000000)
    db_chat = next(
        (
            chat
            for chat in user.chats
            if chat["id"] == data.object.chat and chat.get("installed")
        ),
        None,
    )
    db_chat_status = "дежурный 🎊" if db_chat else "не держурный 🙅‍♂️"

    edit_message = f"""
    ╔⫷| [id{message.from_id}|Информация о деже]
    ╠⫸| {api_user_data[0].first_name} {api_user_data[0].last_name}
    ╠⫸| Никнейм: [id{message.from_id}|{user.username}]
    ╠⫸| В довах: {len(user.trust_users)}ч.
    ╠⫸| Чатов: {len(user.chats)}шт.
    ╠⫸| Токен валиден
    ║
    ╠⫸| Инфо о чате
    ╠⫸| Iris Id: {data.object.chat}
    ╠⫸| Peer Id: {message.peer_id}
    ╠⫸| Название: {chat.title}
    ╠⫸| Я тут {db_chat_status}
    ║
    ╚⫸| ⚙ <-[IDM LITE]-> ⚙
    """.replace(
        "    ", ""
    )  # хз зачем я про токен написал, но пусть будет

    await api.messages.edit(
        peer_id=message.peer_id,
        message_id=message.id,
        message=edit_message,
        keep_forward_messages=True,
    )

    return {"response": "ok"}
