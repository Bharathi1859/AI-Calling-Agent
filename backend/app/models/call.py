from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import relationship

from app.database import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    provider_call_id = Column(
        String(100),
        nullable=True,
        index=True
    )

    direction = Column(
        String(20),
        default="outbound",
        nullable=False
    )

    status = Column(
        String(30),
        default="initiated",
        nullable=False
    )

    start_time = Column(DateTime, nullable=True)

    end_time = Column(DateTime, nullable=True)

    duration = Column(Integer, nullable=True)

    outcome = Column(String(100), nullable=True)

    lead_status = Column(String(50), nullable=True)

    follow_up_required = Column(
        String(10),
        default="no",
        nullable=False
    )

    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    customer = relationship(
        "Customer",
        back_populates="calls"
    )

    messages = relationship(
        "ConversationMessage",
        back_populates="call",
        cascade="all, delete-orphan"
    )

    summary = relationship(
        "CallSummary",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan"
    )