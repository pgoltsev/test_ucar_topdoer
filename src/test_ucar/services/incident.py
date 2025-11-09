from test_ucar.db.models import IncidentStatusEnum


class IncidentStatusManager:
    # Переходы статусов.
    TRANSITIONS: dict = {
        IncidentStatusEnum.SUBMITTED: (IncidentStatusEnum.ACKNOWLEDGED,),
        IncidentStatusEnum.ACKNOWLEDGED: (IncidentStatusEnum.RESOLVED,),
    }

    @classmethod
    def can_transit(cls, from_status: IncidentStatusEnum, to_status: IncidentStatusEnum) -> bool:
        return to_status in cls.TRANSITIONS.get(from_status, [])
