import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from starlette import status

from test_ucar.db.crud import async_session
from test_ucar.db.models import Incident, IncidentStatusEnum, IncidentSourceEnum
from test_ucar.main import app


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            '/api/v1/incidents/',
            json={
                'description': 'Случилась беда!',
                'status': IncidentStatusEnum.SUBMITTED.value,
                'source': IncidentSourceEnum.OPERATOR.value,
            }
        )

    assert response.status_code == status.HTTP_201_CREATED

    response_data: dict = response.json()
    incident_id: int = response_data['id']
    async with async_session() as session:
        incident: Incident = await session.get(Incident, incident_id)
    assert response_data == {
        'id': incident.id,
        'description': 'Случилась беда!',
        'status': IncidentStatusEnum.SUBMITTED.value,
        'source': IncidentSourceEnum.OPERATOR.value,
        'created_at': incident.created_at.isoformat().replace('+00:00', 'Z'),
    }
