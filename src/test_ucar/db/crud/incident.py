from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
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

        await _set_status(incident_obj, status, session)

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
    async with (async_session() as session):
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


async def set_status(incident: Incident, status: IncidentStatusEnum) -> Incident:
    async with async_session() as session:
        await _set_status(incident, status, session)
        await session.commit()

    return incident


async def _set_status(incident_obj: Incident, status: IncidentStatusEnum, session: AsyncSession) -> None:
    status_obj: IncidentStatus = IncidentStatus(value=status, incident=incident_obj)
    session.add(status_obj)
    await session.flush()

    incident_obj.status = status_obj
