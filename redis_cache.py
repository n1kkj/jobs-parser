import aioredis


class RedisCache:
    def __init__(self, redis_url='redis://localhost:6379/0'):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        if self.redis is None:
            self.redis = await aioredis.from_url(self.redis_url)

    async def set(self, key: str, value: str):
        await self.redis.set(key.encode(), value.encode())

    async def get(self, key: str):
        async with self.redis.client() as conn:
            value = await conn.get(key.encode())

        if value is None:
            return
        return value.decode()

    async def delete(self, kek3):
        async with self.redis.client() as conn:
            await conn.delete(kek3.encode())
