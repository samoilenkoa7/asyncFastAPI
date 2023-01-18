import uuid

from pydantic import BaseModel


class BaseBookingTime(BaseModel):
    available_time_id: uuid.UUID


class DeleteBookingTime(BaseBookingTime):
    pass


class CreateBookingTime(BaseBookingTime):
    pass


class BookingTime(BaseBookingTime):
    id: uuid.UUID

    class Config:
        orm_mode = True
