import time

from pythonping import ping
from vkbottle import API
from vkbottle.user import Message

from app.core import route


@route.signal_handler(commands=["пинг"])
async def ping_handler(message: Message, api: API):
    result = ping("api.vk.com", count=4)
    response_times = result.rtt_avg_ms if result.rtt_avg_ms else result.rtt_avg

    ping_time = time.time() - message.date

    await api.messages.send(
        peer_id=message.peer_id,
        message_id=message.id,
        message=f"🏓 Задержка API VK: {response_times} мс.\n"
        f"🌐 Получил сигнал за: {ping_time:.2f} сек.",
        reply_to=message.id,
        random_id=0,
    )

    return {"response": "ok"}
