import uuid

from fastapi import Depends, Response

from .booking_timeDAL import BookingTimeDAL
from .. import models
from ..pydantic_models.booking_time_model import CreateBookingTime, DeleteBookingTime


class BookingTimeService:
    def __init__(self, db_service: BookingTimeDAL = Depends()):
        self.db_service = db_service

    async def create_new_booking(self,
                                 booking_data: CreateBookingTime,
                                 user_id: uuid.UUID) -> models.BookingTime:
        booking_time = await self.db_service.create_new_booking(booking_data=booking_data, user_id=user_id)
        return booking_time

    async def delete_booking_time(self,
                                  booking_data: DeleteBookingTime,
                                  user_id: uuid.UUID) -> Response:
        await self.db_service.delete_booking(booking_data, user_id)
        return Response(f'Booking data successfully deleted')

    async def get_all_bookings(self,
                               user_id: uuid.UUID) -> list[models.BookingTime]:
        available_time_list = await self.db_service.get_all_bookings_by_user(user_id)
        return available_time_list
