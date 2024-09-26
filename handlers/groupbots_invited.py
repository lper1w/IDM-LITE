from vkbottle import API, VKAPIError
from vkbottle.user import Message
from vkbottle_types.codegen.objects import MessagesConversationPeerType

from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.schemas.iris.methods import IrisDutyEventMethod


@route.method_handler(IrisDutyEventMethod.GROUP_BOTS_INVITED)
async def group_bots_invited(data: IrisDutyEvent, message: Message, api: API):
    peer_id = None
    conversations = await api.messages.get_conversations()

    for conversation in conversations.items:
        if conversation.conversation.peer.type != MessagesConversationPeerType.CHAT:
            continue

        if (
            data.message.conversation_message_id
            <= conversation.last_message.conversation_message_id
            < data.message.conversation_message_id + 300
        ):
            try:
                _conversation = await api.messages.get_by_conversation_message_id(
                    peer_id=conversation.conversation.peer.id,
                    conversation_message_ids=data.message.conversation_message_id,
                )

                message_data = _conversation.items[0]
                if (
                    message_data.from_id == data.message.from_id
                    and message_data.date == data.message.date
                ):
                    peer_id = message_data.peer_id
            except Exception:
                continue

        if not peer_id:
            return {
                "response": "error",
                "error_code": 10,
            }

        group = await api.groups.get_by_id(group_ids=data.object.group_id)

        try:
            await api.method(
                "messages.setMemberRole",
                {
                    "role": "admin",
                    "peer_id": peer_id,
                    "member_id": data.object.group_id,
                },
            )
            await api.messages.send(
                peer_id=message.peer_id,
                message=f"✅ Группа-бот [club{data.object.group_id}|{group[0].name}] назначена на роль администратора.",
            )
        except VKAPIError as e:
            if e.code == 15:
                await api.messages.send(
                    peer_id=message.peer_id,
                    message=f"❗ Нет привилегий для добавления в группу {group[0].title}.",
                    random_id=0,
                )

            await api.messages.send(
                peer_id=message.peer_id,
                message=f"❗ Ошибка при добавлении в группу {group[0].title}. {e}",
                random_id=0,
            )
        finally:
            return {"response": "ok"}
