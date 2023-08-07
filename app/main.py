from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis  # type ignore

from app import menus, models
from app.config import settings
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(menus.router, tags=['Menu'], prefix='/api/v1')
