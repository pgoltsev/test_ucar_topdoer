import pytest
from httpx import AsyncClient
from starlette import status

from test_ucar.db.crud import async_session
from test_ucar.db.models import Incident, IncidentStatusEnum, IncidentSourceEnum


@pytest.mark.asyncio
async def test_create(async_client: AsyncClient):
    async with async_client as ac:
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
