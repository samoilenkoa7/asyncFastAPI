import re
import uuid
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator, EmailStr
from starlette import status

LETTER_MACH_PATTERN = re.compile(r'^[a-zA-Z]+$')
EXCEPTION = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail='Surname and name should contain only letters')


class UserKind(str, Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'


class BaseUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    kind: Optional[UserKind]


class CreateUser(BaseUser):
    password: str

    @validator('name', 'surname')
    def validate_name(cls, value):
        if not LETTER_MACH_PATTERN.match(value):
            raise EXCEPTION
        return value


class User(BaseUser):
    id: uuid.UUID
    is_active: bool

    class Config:
        orm_mode = True
