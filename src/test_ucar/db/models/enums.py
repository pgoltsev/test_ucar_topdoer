from enum import StrEnum, auto


class IncidentStatusEnum(StrEnum):
    SUBMITTED = auto()  # Стартовый статус.
    ACKNOWLEDGED = auto()
    RESOLVED = auto()


class IncidentSourceEnum(StrEnum):
    OPERATOR = auto()
    MONITORING = auto()
    PARTNER = auto()
