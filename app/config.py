import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    if (os.environ["MENU_ENV"] == "app"):
        DATABASE_PORT: int
        POSTGRES_PASSWORD: str
        POSTGRES_USER: str
        POSTGRES_DB: str
        POSTGRES_HOST: str
        POSTGRES_HOSTNAME: str
        REDIS_HOST: str
        REDIS_PORT: int
        REDIS_DB: int

    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    class Config:
        if (os.environ["MENU_ENV"] == "app"):
            env_file = './.env'
        env_file = './.env.test'


settings = Settings()  # type: ignore
