import datetime
import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src import models
from src.database import get_async_session
from src.pydantic_models.available_time_model import CreateAvailableTime, UpdateAvailableTime


class AvailableTimeDAL:
    """Provide database operations with available time model"""
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def check_if_user_is_teacher(self, user_id) -> bool:
        statements = select(models.User).filter(models.User.id == user_id)
        user_instance = await self.session.execute(statements)
        user_instance = user_instance.scalars().one()
        print(user_instance.kind)
        return user_instance.kind == 'teacher'

    async def _get(self, time: datetime.datetime, user_id: uuid.UUID) -> models.AvailableTime:
        print(time, user_id)
        statement = select(models.AvailableTime)\
            .filter(models.AvailableTime.time == time, models.AvailableTime.user_id == user_id)
        available_time_list = await self.session.execute(statement)
        available_time_list = available_time_list.scalars()
        available_time_instance = available_time_list.one()
        return available_time_instance

    async def create_new_available_time(
            self,
            user_id: uuid.UUID,
            available_time_data: CreateAvailableTime
    ) -> models.AvailableTime:
        if await self.check_if_user_is_teacher(user_id):
            available_time_instance = models.AvailableTime(time=available_time_data.time, user_id=user_id)
            self.session.add(available_time_instance)
            await self.session.commit()
            return available_time_instance

    async def get_available_time_by_time(self,
                                         time: datetime.datetime,
                                         user_id: uuid.UUID) -> models.AvailableTime:
        return await self._get(time, user_id)

    async def delete_available_time_by_time(self, time: datetime.datetime, user_id: uuid.UUID) -> None:
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Time with provided user_id and time was not found'
        )
        available_time_instance = await self._get(time, user_id)
        if not available_time_instance:
            raise exception
        await self.session.delete(available_time_instance)
        await self.session.commit()

    async def get_all_available_time(self,
                                     user_id: uuid) -> list[models.AvailableTime]:
        statement = select(models.AvailableTime).filter(models.AvailableTime.user_id == user_id)
        available_time_instances_list = await self.session.execute(statement)
        available_time_instances_list = available_time_instances_list.scalars()
        return [instance for instance in available_time_instances_list]

    async def update_available_time(self,
                                    old_available_time: UpdateAvailableTime,
                                    user_id: uuid.UUID,
                                    new_available_time: UpdateAvailableTime) -> models.AvailableTime:
        available_time_instance = await self._get(time=old_available_time.time, user_id=user_id)
        available_time_instance.time = new_available_time.time
        self.session.add(available_time_instance)
        await self.session.commit()
        return available_time_instance
