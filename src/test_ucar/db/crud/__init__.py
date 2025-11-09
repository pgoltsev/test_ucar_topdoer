from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from test_ucar.config import config

engine = create_async_engine(config.postgres.url)
async_session = async_sessionmaker(engine, expire_on_commit=False)
