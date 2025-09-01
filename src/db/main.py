from sqlmodel import create_engine,text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.books.config import Config
from src.db.models import BooK
from src.db.models import User

async_engine= AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)

async def init_db():
    async with async_engine.begin() as conn:
        """create our database models in the database"""

        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
# Dependency to provide the session object

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
    )
    async with async_session() as session:
        yield session

