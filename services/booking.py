import datetime
import uuid
from typing import Annotated

from fastapi import Depends

import models
from services.base import BaseService


class BookingService(BaseService):
    def __init__(self, db: models.Db):
        super(BookingService, self).__init__(db)

    def remove_booking(self, booking: models.Booking):

        """
        used to remove booking if every appointment in that booking is deleted
        there's no point in leaving empty bookings in the database

        :param booking: models.Booking
        :return: True
        """

        self.remove(booking)
        self.commit()
        return True

    def create_booking(self) -> models.Booking:
        """

        inserts new row into booking table

        :return: new booking
        """

        ref = str(uuid.uuid4())
        booking = models.Booking(created_at=datetime.datetime.now(), booking_reference=ref)
        self.add(booking)
        self.commit()
        return booking

    def handle_booking_appointment(self, booking_ref, appointment):
        """

        # if booking can be found using booking_ref, either remove existing
        # appointment or add new appointment to booking

        :param booking_ref: dict containing decoded jwt payload (bookin_reference as sub)
        :param appointment: models.Appointment
        :return: tuple (done: bool operation: str 'add' | 'remove')
        """

        # hae varaus varausnumerolla
        booking = self.db.query(models.Booking).filter(models.Booking.booking_reference == booking_ref['sub']).first()

        # jos varausta ei ole, ei sille voida myöskään tehdä tapaamista
        if booking is None:
            return False, None

        # jos varaus löytyy, haetaan kaikki sille vuodelle, kuukaudelle, päivälle,
        # tunnille ja minutille varatut tapaamiset
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

        """
        # if an existing appointment can be found, it means that user want's to cancel it


        :param appointment: models.Appointment
        :return: True
        """

        self.remove(appointment)
        self.commit()
        return True

    def _book_appointment(self, booking_ref, appointment):

        """

        :param booking_ref: dict containing decoded jwt payload (bookin_reference as sub)
        :param appointment: models.Appointment
        :return: bool
        """

        booking = self.db.query(models.Booking).filter(models.Booking.booking_reference == booking_ref['sub']).first()
        if booking is None:
            return False

        appointment.booking_id = booking.id
        self.db.add(appointment)
        self.commit()
        return True

    def get_booking_by_ref(self, ref):
        """

        :param ref: str booking_reference
        :return: None | models.Booking
        """
        return self.db.query(models.Booking).filter(models.Booking.booking_reference == ref).first()

    def get_others_appointments(self, booking):

        """

        # find all other appointemnts not linked to my own booking

        :param booking:  models.Booking (my own booking)
        :return: List[models.Appointment]
        """

        if booking is not None:
            appointments = self.db.query(models.Appointment).filter(models.Appointment.booking_id != booking.id).all()
        else:
            appointments = self.db.query(models.Appointment).all()
        return appointments


def get_booking_service(db: models.Db):
    """

    callable to register dependency for FastApi

    :return: BookingService
    """

    return BookingService(db)


BookingServ = Annotated[BookingService, Depends(get_booking_service)]
