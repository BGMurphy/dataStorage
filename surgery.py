from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Surgery(Base):
    """ Surgery info """

    __tablename__ = "surgery_info"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    bookingDate = Column(String(100), nullable=False)
    surgeryDate = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, patient_id, bookingDate, surgeryDate):
        """ Initializes a blood pressure reading """
        self.patient_id = patient_id
        self.bookingDate = bookingDate
        self.surgeryDate = surgeryDate
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['patient_id'] = self.patient_id
        dict['bookingDate'] = self.bookingDate
        dict['surgeryDate'] = self.surgeryDate

        return dict
