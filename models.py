# coding: utf-8
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

engine = create_engine('mysql+mysqlconnector://root:@localhost/fastapivaraus')
conn = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    booking_reference = Column(String(255), nullable=False, unique=True)


class Appointment(Base):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    min = Column(Integer, nullable=False)
    booking_id = Column(ForeignKey('booking.id'), nullable=False, index=True)

    booking = relationship('Booking')


def get_db():
    db = None
    try:
        db = conn()
        yield db
    finally:
        if db is not None:
            db.close()


Db = Annotated[Session, Depends(get_db)]
