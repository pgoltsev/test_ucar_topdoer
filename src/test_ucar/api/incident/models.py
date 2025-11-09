from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, AliasPath

from test_ucar.db.models import IncidentStatusEnum, IncidentSourceEnum


class IncidentBaseModel(BaseModel):
    description: str
    status: IncidentStatusEnum | None = IncidentStatusEnum.SUBMITTED
    source: IncidentSourceEnum


class IncidentCreateModel(IncidentBaseModel):
    ...


class IncidentReadModel(IncidentBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: IncidentStatusEnum = Field(validation_alias=AliasPath('status', 'value'))


class IncidentListModel(BaseModel):
    offset: int
    items: list[IncidentReadModel]


class IncidentStatusUpdateModel(BaseModel):
    status: IncidentStatusEnum


class IncidentFilterParams(BaseModel):
    model_config = ConfigDict(extra='forbid')

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    status: list[IncidentStatusEnum] = []
