import uuid
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(100), nullable=False)
    surname = sa.Column(sa.String(100), nullable=False)
    email = sa.Column(sa.String(200), unique=True, nullable=False)
    hashed_password = sa.Column(sa.String())
    kind = sa.Column(sa.String(10), default='student')
    is_active = sa.Column(sa.Boolean(), default=True)

    available_time = relationship('AvailableTime', backref='teacher')


class AvailableTime(Base):
    __tablename__ = 'available_time'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time = sa.Column(sa.DateTime(), nullable=False)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
