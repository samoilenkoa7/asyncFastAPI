from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import settings


async_engine = create_async_engine(
    settings.database_url,
    future=True,
    echo=True
)


async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_async_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
