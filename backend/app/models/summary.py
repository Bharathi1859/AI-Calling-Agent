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


class CallSummary(Base):
    __tablename__ = "call_summaries"

    id = Column(Integer, primary_key=True, index=True)

    call_id = Column(
        Integer,
        ForeignKey("calls.id"),
        nullable=False,
        unique=True
    )

    requirement = Column(Text, nullable=True)

    capacity = Column(String(100), nullable=True)

    location = Column(String(150), nullable=True)

    application = Column(String(150), nullable=True)

    budget = Column(String(100), nullable=True)

    timeline = Column(String(100), nullable=True)

    customer_intent = Column(String(100), nullable=True)

    key_points = Column(Text, nullable=True)

    follow_up_required = Column(
        String(10),
        default="no",
        nullable=False
    )

    summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    call = relationship(
        "Call",
        back_populates="summary"
    )