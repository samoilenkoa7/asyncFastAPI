import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from pydantic import BaseModel, validator


class BaseAvailableTime(BaseModel):
    time: datetime.datetime

    @validator('time')
    def validate_time(cls, value):
        value = value.replace(tzinfo=None)
        return value


class UpdateAvailableTime(BaseAvailableTime):
    pass


class CreateAvailableTime(BaseAvailableTime):
    pass


class AvailableTime(BaseAvailableTime):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True
