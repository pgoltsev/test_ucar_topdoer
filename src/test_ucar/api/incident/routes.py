from typing import Annotated

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from test_ucar.api.incident.models import IncidentCreateModel, IncidentReadModel, IncidentStatusUpdateModel, \
    IncidentListModel, IncidentFilterParams
from test_ucar.db.crud import incident as incident_crud
from test_ucar.db.models import Incident

router = APIRouter(
    prefix='/incidents',
    tags=['Incidents'],
)


@router.get('/', response_model=IncidentListModel, status_code=status.HTTP_200_OK)
async def get_incidents(filter_query: Annotated[IncidentFilterParams, Query()]):
    """
    Позволяет получить список инцидентов.
    :param filter_query: Параметры фильтрации.
    :return: Список инцидентов.
    """
    objs: list[Incident] = await incident_crud.filter_by(
        statuses=filter_query.status,
        offset=filter_query.offset,
        limit=filter_query.limit,
    )
    return {
        'offset': filter_query.offset + len(objs),
        'items': objs,
    }


@router.post('/', response_model=IncidentReadModel, status_code=status.HTTP_201_CREATED)
async def create_incident(item: IncidentCreateModel):
    """
    Создает инцидент.
    :param item: Данные инцидента.
    :return: Созданный инцидент.
    """
    obj: Incident = await incident_crud.create(**item.model_dump())
    return obj


@router.patch('/{incident_id}/', response_model=IncidentReadModel, status_code=status.HTTP_200_OK)
async def update_incident_status(incident_id: int, item: IncidentStatusUpdateModel):
    """
    Обновляет статус существующего инцидента.
    :param incident_id: ID инцидента для обновления.
    :param item: Объект с новым статусом инцидента.
    :return: Обновленный инцидент.
    """
    obj: Incident | None = await incident_crud.get(id_=incident_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await incident_crud.set_status(incident=obj, status=item.status)
    return obj
