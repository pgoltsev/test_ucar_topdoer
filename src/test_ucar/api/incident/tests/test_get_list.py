import pytest
from httpx import AsyncClient
from starlette import status

from test_ucar.db.crud import incident as incident_crud
from test_ucar.db.models import Incident, IncidentStatusEnum, IncidentSourceEnum


@pytest.mark.asyncio
async def test_filter_by_status(async_client: AsyncClient):
    expected_incidents: list[Incident] = [
        await incident_crud.create(
            description=f'Что-то случилось {_}!',
            status=IncidentStatusEnum.RESOLVED,
            source=IncidentSourceEnum.PARTNER,
        )
        for _ in range(3)
    ]
    # Add one with unexpected status for exclusion.
    await incident_crud.create(
        description='Что-то случилось!',
        status=IncidentStatusEnum.ACKNOWLEDGED,
        source=IncidentSourceEnum.PARTNER,
    )

    async with async_client as ac:
        response = await ac.get('/api/v1/incidents/', params={
            'offset': 0,
            'limit': 10,
            'status': IncidentStatusEnum.RESOLVED.value,
        })

    assert response.status_code == status.HTTP_200_OK
    response_data: dict = response.json()
    assert response_data == {
        'offset': 3,
        'items': [
            {
                'id': incident.id,
                'description': incident.description,
                'status': IncidentStatusEnum.RESOLVED.value,
                'source': IncidentSourceEnum.PARTNER.value,
                'created_at': incident.created_at.isoformat().replace('+00:00', 'Z'),
            }
            for incident in sorted(expected_incidents, key=lambda _: _.created_at, reverse=True)
        ]
    }
