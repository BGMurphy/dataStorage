from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Xray(Base):
    """ X-ray info """

    __tablename__ = "xRay_info"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    result = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, patient_id, result, timestamp):
        """ Initializes a heart rate reading """
        self.patient_id = patient_id
        self.result = result
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}
        dict['id'] = self.id
        dict['patient_id'] = self.patient_id
        dict['result'] = self.result
        dict['timestamp'] = self.timestamp

        return dict
