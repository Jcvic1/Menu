from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

POSTGRES_URL = (
    'postgresql://'
    f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
    f'@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}'
    f'/{settings.POSTGRES_DB}'
)


# POSTGRES_URL=f"postgresql://Jcvic1:16pUqGAJwrCt@ep-shy-mountain-213281-pooler.eu-central-1.aws.neon.tech/test?options=endpoint%3Dep-shy-mountain-213281"

engine = create_engine(POSTGRES_URL, echo=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
