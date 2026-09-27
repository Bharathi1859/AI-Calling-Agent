from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(String(20), nullable=False, unique=True, index=True)

    company_name = Column(String(150), nullable=True)

    purpose = Column(Text, nullable=True)

    product = Column(String(150), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    calls = relationship(
        "Call",
        back_populates="customer",
        cascade="all, delete-orphan"
    )