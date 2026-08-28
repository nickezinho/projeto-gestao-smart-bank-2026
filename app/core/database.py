from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import get_settings

db = create_async_engine(
    get_settings.database_url,
    echo=True
)

AsyncSessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=db
)

Base = declarative_base()