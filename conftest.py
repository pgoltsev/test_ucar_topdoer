import pytest
from httpx import AsyncClient, ASGITransport

from test_ucar.main import app


@pytest.fixture
def async_client():
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )
