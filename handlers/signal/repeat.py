from vkbottle import API
from vkbottle.user import Message

from app.config import settings
from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.services.iris import IrisService


@route.signal_handler(commands=["повтори", "скажи"])
async def repeat_handler(
    api: API, message: Message, data: IrisDutyEvent, service: IrisService
):
    user = service.get_user(id=settings.id)

    if data.message.from_id not in user.trust_users:
        await api.messages.send(
            peer_id=message.peer_id,
            message="⚠️ Вы в списке доверенных пользователей.",
            random_id=0,
            keep_forward_messages=True,
            reply_to=message.id,
        )
        return {"response": "ok"}

    signal_value = data.object.value
    additional_text = signal_value[len("повтори") :].strip()

    await api.messages.send(
        peer_id=message.peer_id,
        message=additional_text,
        random_id=0,
        keep_forward_messages=True,
    )

    return {"response": "ok"}
