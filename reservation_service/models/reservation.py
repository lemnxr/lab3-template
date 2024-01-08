from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Date
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from config.db_connect import DB
from models.hotel import HotelModel


class ReservationModel(DB.Base):
    __tablename__ = "reservation"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    reservation_uid = Column(UUID(as_uuid=True), default=uuid4, nullable=False, unique=True)
    username = Column(String(80), nullable=False)
    payment_uid = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    hotel_id = Column(Integer, ForeignKey(HotelModel.id))
    status = Column(String(20), nullable= False)
    start_date = Column(Date)
    end_date = Column(Date)
    