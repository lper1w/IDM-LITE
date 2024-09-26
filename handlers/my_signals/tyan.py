import io

import aiohttp
from vkbottle import API
from vkbottle.user import Message

from app.core import route


async def fetch_image(api: API) -> tuple[str, list]:
    async with api.requests_session.get(
        "https://api.waifu.pics/nsfw/waifu"
    ) as response:
        parsed_response = await api.parse_json_body(response)
        return parsed_response["url"]


async def upload_image(api: API, url: str) -> dict:
    async with api.requests_session.get(url) as response:
        image = io.BytesIO(await response.read())
        image.name = "tyan.png"

    upload = await api.photos.get_messages_upload_server()
    form_data = aiohttp.FormData()
    form_data.add_field("photo", image, filename="tyan.png", content_type="image/jpeg")

    async with api.requests_session.post(upload.upload_url, data=form_data) as response:
        return await api.parse_json_body(response)


@route.my_signal_handler(commands=["тян"])
async def get_tyan(message: Message, api: API):
    await api.messages.edit(
        peer_id=message.peer_id,
        message_id=message.id,
        message="🎊 Ожидай свою тян 🎊",
    )

    try:
        url = await fetch_image(api)

        upload_data = await upload_image(api, url)
        server = upload_data.get("server")
        photo = upload_data.get("photo")
        photo_hash = upload_data.get("hash")

        attachs = await api.photos.save_messages_photo(
            server=server, photo=photo, hash=photo_hash
        )

        attachment = (
            f"photo{attachs[0].owner_id}_{attachs[0].id}_{attachs[0].access_key}"
        )

        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message="🌟 Твоя фотка",
            attachment=attachment,
        )
    except Exception as e:
        await api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message=f"Произошла ошибка: {str(e)}",
        )

    return {"response": "ok"}
