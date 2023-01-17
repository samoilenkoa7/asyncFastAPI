import datetime
import uuid

from fastapi import Depends, Response

from .available_timeDAL import AvailableTimeDAL
from src import models
from src.pydantic_models.available_time_model import CreateAvailableTime, UpdateAvailableTime


class AvailableTimeService:
    """Business logic for operation with available time"""
    def __init__(self, db_service: AvailableTimeDAL = Depends()):
        self.db_service = db_service

    async def create_available_time(
            self,
            available_time_data: CreateAvailableTime,
            user_id: uuid.UUID) -> models.AvailableTime:
        return await self.db_service.create_new_available_time(user_id, available_time_data)

    async def get_available_time_by_time(
            self,
            time: datetime.datetime,
            user_id: uuid.UUID) -> models.AvailableTime:
        return await self.db_service.get_available_time_by_time(time, user_id)

    async def delete_available_time_by_time(
            self,
            time: datetime.datetime,
            user_id: uuid.UUID) -> Response:
        await self.db_service.delete_available_time_by_time(time, user_id)
        return Response(f'Available time `{time}`: deleted.')

    async def get_all_available_time_by_user(self,
                                             user_id: uuid) -> list[models.AvailableTime]:
        available_time_list = await self.db_service.get_all_available_time(user_id)
        return available_time_list

    async def update_available_time(self,
                                    user_id: uuid.UUID,
                                    old_available_time: UpdateAvailableTime,
                                    new_available_time: UpdateAvailableTime) -> models.AvailableTime:
        updated_available_time = await self.db_service.update_available_time(
            old_available_time,
            user_id,
            new_available_time
        )
        return updated_available_time
