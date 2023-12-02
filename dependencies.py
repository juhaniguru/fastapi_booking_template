from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException

import models
from services.booking import BookingServ
from utils.app_token import AppToken


def get_token():
    return AppToken()


BookingToken = Annotated[AppToken, Depends(get_token)]


def require_booking_ref(_token: BookingToken, service: BookingServ, x_booking_ref: str = Header()):
    try:
        _, _booking_ref = x_booking_ref.split(' ')
        payload = _token.validate(_booking_ref)
        booking = service.get_booking_by_ref(payload['sub'])
        if booking is None:
            raise HTTPException(status_code=401, detail='Unauthorized')
        return booking
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))


def check_optional_booking_ref(_token: BookingToken, service: BookingServ,
                               x_booking_ref: Annotated[Optional[str], Header()] = None):
    try:
        if x_booking_ref is not None:
            _, _booking_ref = x_booking_ref.split(' ')

            payload = _token.validate(_booking_ref)
            booking = service.get_booking_by_ref(payload['sub'])
            if booking is None:
                raise HTTPException(status_code=401, detail='Unauthorized')
            return booking
        return None
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))


BookingRef = Annotated[models.Booking, Depends(require_booking_ref)]
OptionalBookingRef = Annotated[models.Booking, Depends(check_optional_booking_ref)]
