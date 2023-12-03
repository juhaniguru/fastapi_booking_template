from fastapi import APIRouter, HTTPException

import models
from dependencies import BookingToken, BookingRef, OptionalBookingRef
from dtos.booking import CreateBookingRes, BookAppointmentReq, GetBookingsRes
from services.booking import BookingServ

router = APIRouter(prefix='/api/v1/booking', tags=['booking'])


@router.post('/', response_model=CreateBookingRes)
async def create_booking(service: BookingServ, _token: BookingToken):
    """

    If you don't have a booking reference, this endopint inserts booking into database and
    creates a jwt containing the booking_reference

    :param service: BookingServ data access layer
    :param _token: BookingToken to create and validate token for booking_reference
    :return: jwt containing booking_reference as sub attribute {token: str}
    """

    booking = service.create_booking()
    token_str = _token.create({'sub': booking.booking_reference})
    return {'token': token_str}


@router.get('/', response_model=GetBookingsRes)
async def get_bookings(_booking: OptionalBookingRef, service: BookingServ):
    """
    returns all bookings yours and others'

    :param _booking: OptionalBookinRef: bookin_reference jwt
    :param service: BookingServ to add appointments to a booking
    :return: List of all bookings own and others' [{id: int, hour: str, min: str own: bool}]
    """

    appointments = []

    if _booking is not None:
        for a in _booking.appointments:
            appointments.append({
                'id': a.id,
                'hour': str(a.hour),
                'min': '00' if a.min == 0 else str(a.min),
                'own': True
            })
    others_appointments = service.get_others_appointments(_booking)
    for a in others_appointments:
        appointments.append({
            'id': a.id,
            'hour': str(a.hour),
            'min': '00' if a.min == 0 else str(a.min),
            'own': False
        })

    return {'bookings': appointments}


@router.delete('/')
async def remove_booking(_booking: BookingRef, service: BookingServ):
    service.remove_booking(_booking)
    return ""


@router.post('/appointment/')
async def book_appointment(req: BookAppointmentReq, _token: BookingToken, service: BookingServ):
    """

    :param req: Pydantic class containing year, month, day, hour, min and booking_refenrence
    :param _token: BookingToken to get the booking reference out of that jwt
    :param service: BookingServ data access layer
    :return: dict {'operation': 'add' | 'remove', done: True | False}
    """

    booking = _token.validate(req.booking_reference)

    appointment = models.Appointment(year=req.year, month=req.month, day=req.day, hour=req.hour, min=req.min)
    done, operation = service.handle_booking_appointment(booking, appointment)
    if not done:
        raise HTTPException(detail='error booking appointment', status_code=404)
    return {
        'operation': operation,
        'done': done
    }
