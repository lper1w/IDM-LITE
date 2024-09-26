from vkbottle import API
from vkbottle.user import Message

from app.config import settings
from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.services.iris import IrisService


@route.signal_handler(commands=["инфо"])
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

    send_message = f"""
    ╔⫷| [id{message.from_id}|Информация о деже]
    ╠⫸| {api_user_data[0].first_name} {api_user_data[0].last_name}
    ╠⫸| Никнейм: [id{message.from_id}|{user.username}]
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
    )

    await api.messages.send(
        peer_id=message.peer_id,
        message=send_message,
        keep_forward_messages=True,
        random_id=0,
        reply_to=message.id,
    )

    return {"response": "ok"}
