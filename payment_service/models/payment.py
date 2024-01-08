from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from config.db_connect import DB

class PaymentModel(DB.Base):
    __tablename__ = "payments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    payment_uid = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    status = Column(String(20), nullable= False)
    price = Column(Integer, nullable=False)
