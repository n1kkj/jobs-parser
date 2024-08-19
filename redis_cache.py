import redis

import settings


class RedisCache:
    def __init__(self, redis_url=settings.REDIS_DATABASE_URL):
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(self.redis_url)

    def disconnect(self):
        self.redis.close()

    def set(self, key: str, value: str):
        self.redis.set(key.encode(), value.encode())

    def get(self, key: str):
        value = self.redis.get(key)
        if value is None:
            return
        return value.decode()

    def get_all_keys(self):
        return [key.decode() for key in self.redis.keys()]

    def delete(self, key):
        self.redis.delete(key.encode())
