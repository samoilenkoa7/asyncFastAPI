from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_async_session
from src.models import User

from src.pydantic_models import user_model


class UserDAL:
    """User data accel layer for database
     operations with user model"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create_user(self, user_data: user_model.CreateUser) -> User:
        """Creating User instance and adding to session"""
        new_user = User(
            name=user_data.name,
            surname=user_data.surname,
            email=user_data.email,
            hashed_password=user_data.password,
            kind=user_data.kind,
            mailchimp_list_id=user_data.mailchimp_list_id
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        users = await self.session.execute(statement)
        users = users.scalars()
        user = users.one()
        return user

