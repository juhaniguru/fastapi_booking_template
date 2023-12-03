import datetime
import uuid
from typing import Annotated

from fastapi import Depends

import models
from services.base import BaseService


class BookingService(BaseService):
    def __init__(self, db: models.Db):
        super(BookingService, self).__init__(db)

    def create_booking(self) -> models.Booking:
        ref = str(uuid.uuid4())
        booking = models.Booking(created_at=datetime.datetime.now(), booking_reference=ref)
        self.add(booking)
        self.commit()
        return booking

    def handle_booking_appointment(self, booking_ref, appointment):
        """
        Lisää tai poistaa ajan varaukselle / varaukselta

        """

        # hae varaus varausnumerolla
        booking = self.db.query(models.Booking).filter(models.Booking.booking_reference == booking_ref['sub']).first()

        # jos varausta ei ole, ei sille voida myöskään tehdä tapaamista
        if booking is None:
            return False, None

        # jos varaus löytyy, haetaan kaikki sille vuodelle, kuukaudelle, päivälle, tunnille ja minutille varatut tapaamiset
        q = self.db.query(models.Appointment).filter(

            (models.Appointment.year == appointment.year) &
            (models.Appointment.month == appointment.month) &
            (models.Appointment.day == appointment.day) &
            (models.Appointment.hour == appointment.hour) &
            (models.Appointment.min == appointment.min))

        existing_appointments = q.all()

        # jos varattuja tapaamisia ei ole, voidaan varata tapaaminen
        if len(existing_appointments) == 0:
            return self._book_appointment(booking_ref, appointment), 'add'
        found = None

        # jos varattuja tapaamisia on, varmistetaan, että varatuista tapaamisista löytyy oikea varaustunnus
        for existing_appointment in existing_appointments:
            if existing_appointment.booking_id == booking.id:
                found = existing_appointment
                break

        # jos oikeaa varaustunnusta ei löydy, joku yrittää poistaa toisen varaamaa tapaamista
        if found is None:
            return False, None

        # jos aika löytyy ja sillä on oikea varaustunnus, silloin käyttäjä klikkaa jo varattua aikaa
        # ja se tapaaminen perutaan
        return self._remove_appointment(found), 'remove'

    def _remove_appointment(self, appointment):
        self.remove(appointment)
        self.commit()
        return True

    def _book_appointment(self, booking_ref, appointment):
        booking = self.db.query(models.Booking).filter(models.Booking.booking_reference == booking_ref['sub']).first()
        if booking is None:
            return False

        appointment.booking_id = booking.id
        self.db.add(appointment)
        self.commit()
        return True

    def get_booking_by_ref(self, ref):
        return self.db.query(models.Booking).filter(models.Booking.booking_reference == ref).first()

    def get_others_appointments(self, booking):

        if booking is not None:
            appointments = self.db.query(models.Appointment).filter(models.Appointment.booking_id != booking.id).all()
        else:
            appointments = self.db.query(models.Appointment).all()
        return appointments



def get_booking_service(db: models.Db):
    return BookingService(db)


BookingServ = Annotated[BookingService, Depends(get_booking_service)]
