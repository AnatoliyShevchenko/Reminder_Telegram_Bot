# Python
from typing import Any
import pickle

# Local
from src.settings.base import AIOREDIS


class RedisUtils:
    """Class for working with Redis."""

    async def set_object_to_redis(
        self, obj: Any, chat_id: int,
        key: str, ttl: int = None
    ) -> None:
        """
        Function for store some data in redis.
        ttl is a time to live(in seconds).
        """
        value = pickle.dumps(obj=obj)
        await AIOREDIS.set(
            name=f"{chat_id}_{key}", value=value, ex=ttl
        )
        return

    async def get_object_from_redis(
        self, chat_id: int, key: str
    ) -> Any | None:
        """Function for get data from redis."""
        try:
            value = await AIOREDIS.get(name=f"{chat_id}_{key}")
            obj: Any = pickle.loads(value)
            return obj
        except:
            return None
        
    async def values_to_list_in_redis(
        self, *args, chat_id: int, key: list|str
    ) -> None:
        """
        Push messages ID to list in Redis, 
        recieving unlimited arguments for push to Redis.
        """
        if isinstance(key, list):
            for k in key:
                await AIOREDIS.rpush(name=f"{chat_id}_{k}", *args)
        elif isinstance(key, str):
            await AIOREDIS.rpush(f"{chat_id}_{key}", *args)

    async def get_list_from_redis(
        self, chat_id: int, key: list|str
    ):
        """
        Get list with messages ID for remove this messages from chat.
        """
        if isinstance(key, str):
            result = await AIOREDIS.lrange(f"{chat_id}_{key}", 0, -1)
            return [value.decode() for value in result]
        elif isinstance(key, list):
            result: list = []
            for k in key:
                data = await AIOREDIS.lrange(f"{chat_id}_{k}", 0, -1)
                for value in data:
                    result.append(value.decode())
            return result

    async def clear_user_data(self, chat_id: int):
        keys = await AIOREDIS.keys()
        for key in keys:
            if str(chat_id) in str(key):
                await AIOREDIS.delete(key)

    async def destroy_all_data(self):
        await AIOREDIS.flushall()

