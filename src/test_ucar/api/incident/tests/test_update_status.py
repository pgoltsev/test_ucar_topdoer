import pytest
from httpx import AsyncClient
from starlette import status

from test_ucar.db.crud import incident as incident_crud
from test_ucar.db.models import Incident, IncidentStatusEnum, IncidentSourceEnum


@pytest.mark.asyncio
async def test_update_status(async_client: AsyncClient):
    incident: Incident = await incident_crud.create(
        description='Что-то случилось!',
        status=IncidentStatusEnum.SUBMITTED,
        source=IncidentSourceEnum.PARTNER,
    )

    async with async_client as ac:
        response = await ac.patch(
            f'/api/v1/incidents/{incident.id}/',
            json={
                'status': IncidentStatusEnum.ACKNOWLEDGED.value,
            })

    assert response.status_code == status.HTTP_200_OK
    response_data: dict = response.json()
    assert response_data == {
        'id': incident.id,
        'description': 'Что-то случилось!',
        'status': 'acknowledged',
        'source': 'partner',
        'created_at': incident.created_at.isoformat().replace('+00:00', 'Z'),
    }
    incident = await incident_crud.get(incident.id)
    assert incident.status.value == IncidentStatusEnum.ACKNOWLEDGED


@pytest.mark.asyncio
async def test_update_status_of_missing(async_client: AsyncClient):
    async with async_client as ac:
        response = await ac.patch(
            f'/api/v1/incidents/-1/status',
            json={
                'status': IncidentStatusEnum.ACKNOWLEDGED.value,
            })

    assert response.status_code == status.HTTP_404_NOT_FOUND
