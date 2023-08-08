from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app import models
from app.config import settings
from app.database import engine
from app.menu_endpoints import dish, menu, submenu

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


app.include_router(menu.router, tags=['Menu'], prefix='/api/v1')
app.include_router(submenu.router, tags=['Submenu'], prefix='/api/v1')
app.include_router(dish.router, tags=['Dish'], prefix='/api/v1')
