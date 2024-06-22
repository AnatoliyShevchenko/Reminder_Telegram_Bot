# AioHTTP
import aiohttp
from aiohttp import ClientSession

# Local
from src.settings.base import SERVER_URL, logger


async def get_user(telegram_id: int):
    try:
        async with ClientSession() as session:
            async with session.get(
                url=f"{SERVER_URL}users/{telegram_id}"
            ) as response:
                if response.status == 200:
                    content = await response.json()
                    logger.info(msg=content)
                    return True, content
                else:
                    content = await response.json()
                    logger.warning(msg=content)
                    return False, content
    except aiohttp.ClientError as e:
        logger.error(msg=f"Request failed: {e}")
        return False, str(e)
    
async def create_user(chat_id: int, timezone: int, language: str):
    try:
        async with ClientSession() as session:
            async with session.post(
                url=f"{SERVER_URL}users", json={
                    "telegram_id": chat_id,
                    "language": language,
                    "timezone": timezone
                }
            ) as response:
                if response.status == 200:
                    content = await response.json()
                    return True, content
                else:
                    content = await response.json()
                    logger.warning(msg=content)
                    return False, content
    except aiohttp.ClientError as e:
        logger.error(msg=f"Request failed: {e}")
        return False, str(e)

