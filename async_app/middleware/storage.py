from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_session import SimpleCookieStorage

from redis.asyncio import Redis

session_storage_middleware = session_middleware(
    # SimpleCookieStorage()

    RedisStorage(
        Redis(host='localhost', port=6379),
    ),
)
