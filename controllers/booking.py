from fastapi import APIRouter, HTTPException

import models
from dependencies import BookingToken
from dtos.booking import CreateBookingRes, BookAppointmentReq
from services.booking import BookingServ

router = APIRouter(prefix='/api/v1/booking', tags=['booking'])


@router.post('/', response_model=CreateBookingRes)
async def create_booking(service: BookingServ, _token: BookingToken):
    booking = service.create_booking()
    token_str = _token.create({'sub': booking.booking_reference})
    return {'token': token_str}


@router.post('/appointment/')
async def book_appointment(req: BookAppointmentReq, _token: BookingToken, service: BookingServ):

    booking = _token.validate(req.booking_reference)

    appointment = models.Appointment(year=req.year, month=req.month, day=req.day, hour=req.hour, min=req.min)
    done, operation = service.handle_booking_appointment(booking, appointment)
    if not done:
        raise HTTPException(detail='error booking appointment', status_code=404)
    return {
        'operation': operation,
        'done': done
    }


