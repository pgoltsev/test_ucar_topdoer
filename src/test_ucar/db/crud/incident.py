from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, contains_eager

from test_ucar.db.crud import async_session
from test_ucar.db.models import IncidentStatusEnum, IncidentSourceEnum, Incident, IncidentStatus


async def create(description: str, status: IncidentStatusEnum, source: IncidentSourceEnum) -> Incident:
    async with async_session() as session:
        incident_obj: Incident = Incident(
            description=description,
            source=source,
        )
        session.add(incident_obj)
        await session.flush()

        status_obj: IncidentStatus = IncidentStatus(value=status, incident=incident_obj)
        session.add(status_obj)
        await session.flush()

        incident_obj.status = status_obj

        await session.commit()

    return incident_obj


async def get(id_: int) -> Incident | None:
    async with async_session() as session:
        obj: Incident | None = (await session.scalars(
            select(Incident).
            options(joinedload(Incident.status)).
            where(Incident.id == id_)
        )).first()
    return obj


async def filter_by(
    statuses: list[IncidentStatusEnum],
    offset: int,
    limit: int,
) -> list[Incident]:
    filters = []
    if statuses:
        filters.append(IncidentStatus.value.in_(statuses))
    async with async_session() as session:
        stmt = (
            select(Incident)
            .join(Incident.status).
            options(
                contains_eager(Incident.status).
                load_only(IncidentStatus.value)
            ).order_by(Incident.created_at.desc()).
            limit(limit).offset(offset)
        )
        if filters:
            stmt = stmt.where(*filters)
        objs = await session.scalars(stmt)
    return list(objs)


async def set_status(incident: Incident, status: IncidentStatusEnum) -> bool:
    """
    Обновляет статус инцидента по его ID.
    :param incident: Инцидент, у которого надо обновить статус.
    :param status: Новый статус.
    :return: True, если статус инцидента был успешно обновлен, иначе - False.
    """
    success: bool = False

    async with async_session() as session:
        # Создаем новый статус.
        status_obj: IncidentStatus = IncidentStatus(value=status, incident=incident)
        session.add(status_obj)
        await session.flush()

        # Обновляем статус у инцидента.
        # Статус обновляется только если у инцидента в момент обновления ожидаемый активный статус.
        stmt = (
            update(Incident)
            .where(
                Incident.id == incident.id,
                Incident.status_id == incident.status.id,
            ).values(status_id=status_obj.id).returning(Incident.id)
        )
        success = (await session.scalars(stmt)).first() is not None
        if success:
            # Если инцидент с нужным статусом найден и статус обновлен.
            await session.commit()

    return success
