from typing import Any, Optional
import aioredis
import json

from app.utilities.settings import Settings

# TODO: update the implementation once migrated to aioredis>2.0
class Redis:
    
    settings = Settings()
    
    async def connect(
        self
    ):
        redis = await aioredis.create_redis_pool(
            address=f'redis://{self.settings.redis_endpoint}:{self.settings.redis_port}',
            password=self.settings.redis_auth,
        )

        return redis

    async def set(
        self,
        key: str,
        value: Any,
        expiry: Optional[int] = 0
    ):
        connection = await self.connect()
        value = await connection.set(
            key=key,
            value=value,
            expire=expiry
        )
        return value

    async def get(
        self,
        key: str
    ):
        connection = await self.connect()
        value = await connection.get(key)
        return value

    async def get_dict(
        self,
        key: str
    ):
        connection = await self.connect()
        value = await connection.get(key)
        return json.loads(value) if value else None

    async def flushdb(
        self,
    ):
        connection = await self.connect()
        await connection.flushdb()