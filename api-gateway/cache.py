import json
import redis.asyncio as aioredis

class CacheManager:
    def __init__(self, url, ttl=3600):
        self.url, self.ttl = url, ttl
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.url)

    async def get(self, key):
        v = await self.redis.get(f"cache:{key}")
        return json.loads(v) if v else None

    async def set(self, key, val):
        await self.redis.setex(f"cache:{key}", self.ttl, json.dumps(val))
