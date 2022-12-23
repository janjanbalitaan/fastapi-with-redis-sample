from typing import List, Optional
from fastapi import APIRouter, HTTPException
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
import json

from app.data.data import Data
from app.utilities.settings import Settings
from app.utilities.redis import Redis
from app.types.products import Product, UpdateProduct
from app.types.responses import HTTPError, HTTPSuccess

products_router = APIRouter()
data = Data()
settings = Settings()
redis = Redis()
redis_key = f'{settings.redis_namespace}:all-products'

# this get all will just show how to use aiocache to cache all the data that was used in the response
@products_router.get(
    '/all',
    response_model=List[Product],
)
@cached(
    # ttl is in seconds
    # None = no expiry
    ttl=None,
    cache=Cache.REDIS,
    endpoint=settings.redis_endpoint,
    port=settings.redis_port,
    serializer=JsonSerializer(),
    namespace=settings.redis_namespace,
    # set this if the redis have auth
    password=settings.redis_auth,
    key="all-products",
)
async def get_all():
    return data.get("products")

@products_router.get(
    '',
    response_model=List[Product],
)
async def get(
    id: Optional[int] = None,
    title: Optional[str] = None,
):
    query_id = True if id else False
    query_title = True if title else False
    ldata = []
    # use redis value if the cache was already set
    redis_value = await redis.get_dict(
        redis_key
    )
    
    print(f'will be getting on redis={redis_value is not None}')
    rows = redis_value if redis_value else data.get("products")
    if not id and not title:
        ldata = rows
    else:
        for row in rows:
            if query_id and query_title:
                if row["id"] == id and row["title"] == title:
                    ldata.append(row)
            else:
                if query_id and row["id"] == id:
                    ldata.append(row)

                if query_title and row["title"] == title:
                    ldata.append(row)

    return ldata

@products_router.post(
    '',
    status_code=201,
    responses={
        201: {
            "model": Product,
            "description": "successfully created a product",
        },
        400: {
            "model": HTTPError,
            "description": "error while creating a product",
        },
    }
)    
async def create(
    payload: Product
):
    try:
        rows = data.get("products")
        for row in rows:
            if row["id"] == payload.id:
                raise Exception(f'id={payload.id} already exists')
        
        is_success, message = data.append(
            "products",
            payload.dict()
        )

        if not is_success:
            raise Exception(message)

        # append also in redis cache if the key are already set
        redis_value = await redis.get_dict(
            redis_key
        )
        if redis_value:
            redis_value.append(
                payload.dict()
            )

            # set the new value for the redis key
            await redis.set(
                redis_key,
                value=json.dumps(redis_value),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')
    
    return payload

@products_router.put(
    '/{id}',
    status_code=200,
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully updated a product",
        },
        400: {
            "model": HTTPError,
            "description": "error while updating a product",
        },
    }
)    
async def update(
    id: int,
    payload: UpdateProduct,
):
    try:
        found = False
        rows = data.get("products")
        for idx, row in enumerate(rows):
            if row["id"] == id:
                rows[idx] = {
                    **payload.dict(),
                    "id": id,
                }
                found = True
        if not found:
            raise Exception(f'{id=} does not exist')
        
        is_success, message = data.create(
            "products",
            rows
        )

        if not is_success:
            raise Exception(message)

        # update in redis cache if the key are already set
        redis_value = await redis.get_dict(
            redis_key
        )
        if redis_value:
            # set the new value for the redis key
            await redis.set(
                redis_key,
                value=json.dumps(rows),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully updated {id=}'
    }

@products_router.delete(
    '/{id}',
    status_code=200,
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully deleted a product",
        },
        400: {
            "model": HTTPError,
            "description": "error while deleting a product",
        },
    }
)    
async def delete(
    id: int
):
    try:
        found = False
        rows = data.get("products")
        for idx, row in enumerate(rows):
            if row["id"] == id:
                rows.pop(idx)
                found = True
        if not found:
            raise Exception(f'{id=} does not exist')
        
        is_success, message = data.create(
            "products",
            rows
        )

        if not is_success:
            raise Exception(message)

        # delete in redis cache if the key are already set
        redis_value = await redis.get_dict(
            redis_key
        )
        if redis_value:
            # set the new value for the redis key
            await redis.set(
                redis_key,
                value=json.dumps(rows),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully deleted {id=}'
    }
