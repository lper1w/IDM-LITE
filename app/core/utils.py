import asyncio
import importlib
import inspect
import os
import re
from typing import Any, AsyncGenerator, Dict, List, Optional

from loguru import logger
from vkbottle import API
from vkbottle.user import Message

from app.core import route
from app.schemas.iris.event import IrisDutyEvent
from app.schemas.iris.methods import IrisDutyEventMethod
from app.services.iris import IrisService


class IrisHandlerManager:
    def __init__(self, service: IrisService, data: IrisDutyEvent, api: API):
        self.service = service
        self.data = data
        self.api = api

    @staticmethod
    def load_handlers():
        handlers_dir = os.path.join("handlers")
        for root, dirs, files in os.walk(handlers_dir):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    module_path = os.path.relpath(
                        os.path.join(root, filename), handlers_dir
                    )
                    module_name = module_path.replace(os.sep, ".")[:-3]
                    importlib.import_module(f"handlers.{module_name}")

    async def search_peer_from_last_message(self) -> Optional[Dict[str, Any]]:
        if not self.data:
            logger.warning("No message data provided for chat search.")
            return None

        user_id = self.data.user_id
        if user_id is None:
            logger.warning("No user_id provided in message data.")
            return None

        user = self.service.get_user(id=user_id)
        current_chats: List[Dict[str, Any]] = user.chats

        existing_chat = next(
            (chat for chat in current_chats if chat["id"] == self.data.object.chat),
            None,
        )

        if existing_chat:
            if not self.data.message:
                history = await self.api.messages.get_history(
                    peer_id=existing_chat["peer_id"]
                )
                return history.items[0]
            else:
                chat = await self.api.messages.search(
                    q=self.data.message.text if self.data.message else None,
                    peer_id=existing_chat["peer_id"],
                    count=1,
                )
                return chat.items[0]

        messages = await self.api.messages.search(q=self.data.message.text, count=5)
        chats = [chat for chat in messages.items if chat.peer_id > 2000000000]
        if not chats:
            logger.warning("No chats found with the given message.")
            return None

        current_chats.append(
            {
                "id": self.data.object.chat,
                "peer_id": chats[0].peer_id,
                "installed": False,
            }
        )

        user.chats = current_chats
        self.service.update_user(user=user)

        return chats[0]

    async def get_all_history(self, peer_id: int, offset: int = 0):
        chat = await self.api.messages.get_history(
            count=1, peer_id=peer_id, offset=offset
        )
        count = chat.count

        while offset < count:
            try:
                chat = await self.api.messages.get_history(
                    count=200, peer_id=peer_id, offset=offset
                )
            except Exception as e:
                logger.error(f"Error fetching chat history: {e}")
                await asyncio.sleep(3)
                continue

            offset += 200
            for item in chat.items:
                yield item

    async def dispatch_handler(self):
        chat = await self.search_peer_from_last_message()

        if not chat:
            logger.warning("Chat not found, unable to proceed with handler.")
            return {"response": "Chat not found"}

        if self.data.method == IrisDutyEventMethod.SEND_MY_SIGNAL:
            command = self.data.object.value.split()[0].lower()
            handler = route.get_my_signal_handler(command)
        elif self.data.method == IrisDutyEventMethod.SEND_SIGNAL:
            signal_value = self.data.object.value.split()[0].lower()
            handler = route.get_signal_handler(signal_value)
        else:
            handler = route.get_handler(self.data.method)

        if handler:
            handler_params = inspect.signature(handler).parameters
            handler_args = {}

            if "handler_manager" in handler_params:
                handler_args["handler_manager"] = self
            if "data" in handler_params:
                handler_args["data"] = self.data
            if "message" in handler_params:
                handler_args["message"] = chat
            if "api" in handler_params:
                handler_args["api"] = self.api
            if "service" in handler_params:
                handler_args["service"] = self.service

            return await handler(**handler_args)

        logger.info(f"No handler found for method: {self.data.method}")
        return {
            "response": "error",
            "error_code": 1,
            "error_message": "Команда не реализована.",
        }

    async def get_by_conversation_message_id(
        self, api: API, peer_id: int, ids: list
    ) -> AsyncGenerator[list, int]:
        data = await api.messages.get_by_conversation_message_id(
            peer_id=peer_id,
            conversation_message_ids=ids,
        )

        for item in data.items:
            yield item.id

    async def search_user_id(self, event: Message) -> int:
        if event.reply_message:
            user_id = event.reply_message.from_id
        elif len(event.text.split(maxsplit=2)) < 3:
            user_id = event.from_id
        else:
            user_id = int(re.findall(r"\d+", event.text)[0])

        return user_id
