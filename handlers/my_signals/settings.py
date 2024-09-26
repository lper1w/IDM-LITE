from vkbottle import API
from vkbottle.user import Message

from app.config import settings
from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.services.iris import IrisService


@route.my_signal_handler(commands=["ник"])
async def change_username_handler(
    data: IrisDutyEvent, message: Message, api: API, service: IrisService
):
    user = service.get_user(id=settings.id)

    if len(data.object.value.split()) < 2:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message="⚠️ Не указан новый никнейм.",
        )
        return {"response": "ok"}

    user.username = data.object.value.split(maxsplit=1)[1]
    service.update_user(user=user)

    await api.messages.edit(
        peer_id=message.peer_id,
        message_id=message.id,
        message=f"✅ Никнейм изменен на [id{message.from_id}|{data.object.value.split(maxsplit=1)[1]}].",
    )

    return {"response": "ok"}
