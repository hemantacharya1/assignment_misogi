from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func

from app.db.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    auto_category = Column(String(100), nullable=True)
    tags = Column(String(255), nullable=True)
    priority = Column(String(50), nullable=True)
    generated_response = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
