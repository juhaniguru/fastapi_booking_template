import datetime
from typing import List

from pydantic import BaseModel


class CreateBookingRes(BaseModel):
    token: str


class Booking(BaseModel):
    id: int
    hour: str
    min: str
    own: bool


class GetBookingsRes(BaseModel):
    bookings: List[Booking]


class BookAppointmentReq(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    min: int
    booking_reference: str


class BookAppointmentRes(BaseModel):
    operation: str
    done: bool
