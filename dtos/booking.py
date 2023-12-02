import datetime

from pydantic import BaseModel


class CreateBookingRes(BaseModel):
    token: str


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



