from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from config.db_connect import DB

class LoyaltyModel(DB.Base):
    __tablename__ = "loyaltys"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), nullable=False, unique=True)
    reservation_count = Column(Integer, nullable=False, default=0)
    status = Column(String(80), nullable= False, default='BRONZE')
    discount = Column(Integer, nullable=False)
