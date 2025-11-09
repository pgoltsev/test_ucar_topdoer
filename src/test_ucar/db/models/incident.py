from sqlalchemy import ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from test_ucar.db.models import Base, TimeableMixin
from test_ucar.db.models.enums import IncidentStatusEnum, IncidentSourceEnum


class Incident(Base, TimeableMixin):
    __tablename__ = 'incidents'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey('incident_statuses.id'), nullable=True, unique=True)
    status: Mapped['IncidentStatus'] = relationship(foreign_keys=[status_id], post_update=True)
    statuses: Mapped[list['IncidentStatus']] = relationship(back_populates='incident',
                                                            foreign_keys='IncidentStatus.incident_id')
    source: Mapped[IncidentSourceEnum] = mapped_column(
        Enum(IncidentSourceEnum, name='incident_source_enum'),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f'Incident(id={self.id!r})'


class IncidentStatus(Base, TimeableMixin):
    __tablename__ = 'incident_statuses'

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey('incidents.id'))
    incident: Mapped['Incident'] = relationship(back_populates='statuses', foreign_keys=[incident_id])
    value: Mapped[IncidentStatusEnum] = mapped_column(
        Enum(IncidentStatusEnum, name='incident_status_enum'),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f'IncidentStatus(id={self.id!r}, value={self.value!r})'
