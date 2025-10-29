from sqlmodel import create_engine,text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.books.config import Config
from src.db.models import BooK
from src.db.models import User
# create_engine: Creates database connection engine
# text: For raw SQL queries
# SQLModel: ORM base class for table definitions
# AsyncEngine: Asynchronous database engine wrapper
# AsyncSession: Async database session for non-blocking operations
# sessionmaker: Factory for creating database sessions
# Imports application configuration and database models
#----------------------------------------------------------------------------------------------------------------
async_engine= AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)
# Line-by-line breakdown:
# AsyncEngine: Wraps a regular engine to support async operations
# create_engine: Creates the core database engine
# url=Config.DATABASE_URL: Database connection string from environment variables
# echo=True: Enables SQL query logging for debugging (shows all SQL queries in console)
# Key keywords:
# AsyncEngine: Enables non-blocking database operations
# echo=True: Development feature for SQL debugging
#-------------------------------------------------------------------------------------------------------------------------
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
# Dependency to provide the session object
# Line-by-line breakdown:
# async def init_db(): Async function to initialize database tables
# async with async_engine.begin() as conn:: Opens async database connection with automatic transaction management
# Duplicate async with block: Code error - should only have one block
# await conn.run_sync(SQLModel.metadata.create_all): Creates all database tables defined in SQLModel classes
# Key keywords:
# async with: Context manager for automatic connection cleanup
# begin(): Starts a database transaction
# run_sync(): Runs synchronous code (create_all) in async context
# SQLModel.metadata.create_all: Creates all tables from model definitions
#---------------------------------------------------------------------------------------------------------------
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
    )
    async with async_session() as session:
        yield session
# Line-by-line breakdown:
# async def get_session() -> AsyncSession:: FastAPI dependency function that yields database sessions
# async_session = sessionmaker(...): Creates a session factory (not the actual session)
# bind=async_engine: Associates sessions with the async database engine
# class_=AsyncSession: Specifies to create AsyncSession instances
# expire_on_commit=False: Keeps object attributes accessible after commit (prevents lazy loading issues)
# async with async_session() as session:: Creates and manages actual session instance
# yield session: Provides session to FastAPI routes via dependency injection