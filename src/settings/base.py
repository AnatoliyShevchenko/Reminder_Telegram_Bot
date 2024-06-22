# Aiogram
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

# Python
import logging
from logging.config import dictConfig
from locale import locale_alias

# Third-Party
from decouple import config
from redis import asyncio as aioredis


BOT_TOKEN = config("BOT_TOKEN")
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_DB = config("REDIS_DB")
SERVER_URL = config("SERVER_URL")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
POOL = aioredis.ConnectionPool.from_url(
    url=REDIS_URL, max_connections=20
)
AIOREDIS = aioredis.Redis(connection_pool=POOL)
TTL = 60*30
storage = RedisStorage(redis=AIOREDIS)
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(storage=storage)
LOCALE = locale_alias.get("ru_ru")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
        },
    },
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
} # Logging config

dictConfig(LOGGING)

logger = logging.getLogger(__name__)

