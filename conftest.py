import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import drop_database, create_database

from test_ucar.config import config
from test_ucar.db.models import Base


# class TestPostgresSettings(PostgresSettings):
#     model_config = create_config_dict('postgres_test')


# pg_settings = TestPostgresSettings()
#
#
# @pytest.fixture
# def anyio_backend():
#     return 'asyncio'

#
# @pytest.fixture(scope='session')
# def test_engine():
#     db_url: str = config.postgres.url
#     create_database(db_url)
#
#     engine = create_async_engine(db_url, connect_args={'check_same_thread': False})
#     Base.metadata.create_all(engine)
#
#     yield engine
#
#     Base.metadata.drop_all(engine)
#     drop_database(db_url)
#
#
# @pytest.fixture(scope='function')
# def db_session(test_engine):
#     session_local = async_sessionmaker(bind=test_engine, autocommit=False, autoflush=False)
#     session = session_local()
#     try:
#         yield session
#     finally:
#         session.close()

#
# @pytest.fixture(scope='function')
# def client(db_session):
#     """Подменяем Depends(get_db), чтобы все запросы шли в тестовую БД."""
#
#     def override_get_db():
#         try:
#             yield db_session
#         finally:
#             pass
#
#     app.dependency_overrides[get_db] = override_get_db
#     with TestClient(app) as c:
#         yield c
