from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from config import settings


class PreBase:

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Функция для генерации сессий к БД."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
