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
    booking = relationship('BookingTime', backref='booking_creator')

    def __repr__(self):
        return f'User {self.name} {self.surname}'


class AvailableTime(Base):
    __tablename__ = 'available_time'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time = sa.Column(sa.DateTime(), nullable=False)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
    booking_info = relationship('BookingTime', uselist=False, backref='available_time_info')

    def __repr__(self):
        return f'Available time at {self.time} \n For user {self.user_id}'


class BookingTime(Base):
    __tablename__ = 'booking_time'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    available_time_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('available_time.id'), unique=True)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))

    def __repr__(self):
        return f'Booking time for user with id {self.user_id} on time id {self.available_time_id}'
