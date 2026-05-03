from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    echo=True
)

Session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with Session() as session:
        yield session

# get_async_session = get_db bilan bir xil
get_async_session = get_db