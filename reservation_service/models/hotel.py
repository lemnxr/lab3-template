from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from config.db_connect import DB

class HotelModel(DB.Base):
    __tablename__ = "hotels"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    hotel_uid = Column(UUID(as_uuid=True), default=uuid4, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    country = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    address = Column(String(255), nullable=False)
    stars = Column(Integer)
    price = Column(Integer, nullable=False)
    reservation_relationship = relationship("ReservationModel")
