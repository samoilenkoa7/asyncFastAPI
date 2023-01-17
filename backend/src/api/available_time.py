import datetime

from fastapi import APIRouter, Depends

from src import models
from src.pydantic_models.available_time_model import AvailableTime, CreateAvailableTime, UpdateAvailableTime
from src.services.auth import get_current_user
from src.services.available_time import AvailableTimeService

router = APIRouter(
    prefix='/available-time'
)


@router.get('/get', response_model=AvailableTime)
async def get_available_time(
        time: datetime.datetime,
        service: AvailableTimeService = Depends(),
        user: models.User = Depends(get_current_user)
):
    return await service.get_available_time_by_time(time, user.id)


@router.post('/create', response_model=AvailableTime)
async def create_available_time(
        available_time_data: CreateAvailableTime,
        service: AvailableTimeService = Depends(),
        user: models.User = Depends(get_current_user)
):
    return await service.create_available_time(available_time_data, user.id)


@router.get('/get-list', response_model=list[AvailableTime])
async def get_list_of_available_time(
        user: models.User = Depends(get_current_user),
        service: AvailableTimeService = Depends()
):
    return await service.get_all_available_time_by_user(user_id=user.id)


@router.delete('/delete')
async def delete_available_time(
        time: datetime.datetime,
        user: models.User = Depends(get_current_user),
        service: AvailableTimeService = Depends(),
):
    return await service.delete_available_time_by_time(time, user.id)


@router.patch('/update', response_model=AvailableTime)
async def partial_update_available_time(
        old_available_time: UpdateAvailableTime,
        new_available_time: UpdateAvailableTime,
        user: models.User = Depends(get_current_user),
        service: AvailableTimeService = Depends(),
):
    return await service.update_available_time(user.id, old_available_time, new_available_time)
