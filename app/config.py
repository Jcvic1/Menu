import os

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str


class AppConfig(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = './.env'


class TestConfig(BaseConfig):
    class Config:
        env_file = './.env.test'


if os.environ['MENU_ENV'] == 'app':
    Settings = AppConfig  # type: ignore
else:
    Settings = BaseConfig  # type: ignore

settings = Settings()
