import contextlib
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger
from vkbottle import API

from app.config import settings
from app.depends import iris_service
from app.repositories.iris import User

api: API | None = None
logger.disable("vkbottle")


load_dotenv()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    global api
    token = os.getenv("TOKEN")

    if token is None:
        logger.error("Token not found")
        raise Exception("Token not found") from ValueError("Token not found")

    user = iris_service.get_user(id=settings.id)

    if not user:
        user_dto = User(
            id=settings.id,
            username=settings.username,
            chats=[],
            secret=settings.secret,
        )
        user = iris_service.create_user(user=user_dto)

    api = API(token=token)

    os.system("clear")
    logger.debug("App started")
    yield
    await api.http_client.close()
    logger.warning("App stopped")


async def get_api() -> API:
    if api is None:
        raise Exception("API instance is not initialized")
    return api


app = FastAPI(lifespan=lifespan)
