from src.serializers.serializers import UUIDSerializer

from fastapi import HTTPException, Depends, BackgroundTasks
from starlette import status
from jose import jwt, JWTError
from pydantic import ValidationError
from datetime import datetime, timedelta

from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer

from src.services.mailchimp_service import MailchimpService
from src.settings import settings
from src.models import User
from src.pydantic_models import user_model

from src.pydantic_models.jwt_token import Token
from src.services.userDAL import UserDAL


oauth2_scheme = OAuth2PasswordBearer('/auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    """Class that provides authentication and JWT token services"""

    EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate provided credentials',
        headers={
            'WWW-Authenticate': 'Bearer'
        },
    )

    @classmethod
    def _create_password_hash(cls, plain_password: str) -> str:
        """Hashes plain password"""
        return bcrypt.hash(plain_password)

    @classmethod
    def _validate_password_hash(cls, hashed_password: str, plain_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def _create_token(cls, user_data: User) -> Token:
        user_data = user_model.User.from_orm(user_data)

        uuid_serializer = UUIDSerializer(user_data.id)
        uuid_serializer.to_representation()
        user_data.id = uuid_serializer.uuid_representation

        now = datetime.utcnow()
        play_load = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': uuid_serializer.uuid_representation,
            'user': user_data.dict(),
        }

        access_token = jwt.encode(
            play_load,
            settings.jwt_secret,
            settings.jwt_algorithm
        )
        return Token(access_token=access_token)

    @classmethod
    def validate_token(cls, token: str) -> user_model.User:
        try:
            play_load = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise cls.EXCEPTION

        user_data = play_load.get('user')

        uuid_serializer = UUIDSerializer(user_data.get('id'))
        uuid_serializer.to_internal_value()
        user_data['id'] = uuid_serializer.uuid_internal

        try:
            user = user_model.User.parse_obj(user_data)
        except ValidationError:
            raise cls.EXCEPTION from None
        return user

    def __init__(self,
                 user_database_service: UserDAL = Depends(),
                 mailchimp_servie: MailchimpService = Depends()):
        self.database_service = user_database_service
        self.mailchimp_service = mailchimp_servie

    async def create_new_user(self,
                              user_data: user_model.CreateUser) -> Token:
        if user_data.kind == 'teacher':
            mailchimp_user_id = self.mailchimp_service.create_new_mailchimp_list(user_data)
            user_data.mailchimp_list_id = mailchimp_user_id
        user_data.password = self._create_password_hash(user_data.password)
        user_instance = await self.database_service.create_user(user_data)
        return self._create_token(user_instance)

    async def authenticate_user(self, email: str, password: str) -> Token:
        user = await self.database_service.get_user_by_email(email)
        if not user:
            raise self.EXCEPTION

        if not self._validate_password_hash(user.hashed_password, password):
            raise self.EXCEPTION

        return self._create_token(user)
