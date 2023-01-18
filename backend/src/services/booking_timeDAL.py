import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src import models
from src.database import get_async_session
from src.pydantic_models.booking_time_model import CreateBookingTime, DeleteBookingTime


class BookingTimeDAL:
    """Class for database operations with Booking Time model"""
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def _get(self, user_id: uuid.UUID, available_time_id: uuid.UUID) -> models.BookingTime:
        statement = select(models.BookingTime)\
            .filter(models.BookingTime.available_time_id == available_time_id,
                    models.BookingTime.user_id == user_id)
        booking_time = await self.session.execute(statement)
        booking_time = booking_time.scalars()
        return booking_time.one()

    async def create_new_booking(self,
                                 booking_data: CreateBookingTime,
                                 user_id: uuid.UUID) -> models.BookingTime:
        new_booking_instance = models.BookingTime(available_time_id=booking_data.available_time_id,
                                                  user_id=user_id)
        self.session.add(new_booking_instance)
        await self.session.commit()
        return new_booking_instance

    async def delete_booking(self,
                             booking_data: DeleteBookingTime,
                             user_id: uuid.UUID) -> None:
        booking_instance = await self._get(user_id=user_id, available_time_id=booking_data.available_time_id)
        if not booking_instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Booking with provided time is not found.')
        await self.session.delete(booking_instance)
        await self.session.commit()

    async def get_all_bookings_by_user(self,
                                       user_id: uuid.UUID) -> list[models.BookingTime]:
        statement = select(models.BookingTime).filter(models.BookingTime.user_id == user_id)
        booking_time_list = await self.session.execute(statement)
        booking_time_list = booking_time_list.scalars()
        return [instance for instance in booking_time_list]
