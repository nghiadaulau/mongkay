from redis.asyncio.client import Redis
from applications.core.settings import settings


class RedisClient(Redis):
    def __init__(self):
        super(RedisClient, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,
        )



