from fastapi import APIRouter, Depends

from src import models
from src.pydantic_models.booking_time_model import BookingTime, CreateBookingTime, DeleteBookingTime
from src.services.auth import get_current_user
from src.services.booking_time import BookingTimeService

router = APIRouter(
    prefix='/booking',
)


@router.get('/get-list', response_model=list[BookingTime])
async def get_all_booking_time(
        service: BookingTimeService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return await service.get_all_bookings(user_id=user.id)


@router.post('/create', response_model=BookingTime)
async def create_new_booking(
        booking_data: CreateBookingTime,
        user: models.User = Depends(get_current_user),
        service: BookingTimeService = Depends(),
):
    return await service.create_new_booking(booking_data, user.id)


@router.delete('/delete')
async def delete_booking_by_time(
        booking_data: DeleteBookingTime,
        user: models.User = Depends(get_current_user),
        service: BookingTimeService = Depends(),
):
    return await service.delete_booking_time(booking_data, user_id=user.id)
