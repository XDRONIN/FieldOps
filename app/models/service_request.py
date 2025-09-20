import enum
from sqlalchemy import Column, Integer, String, DateTime, func, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Urgency(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    urgency = Column(SQLEnum(Urgency), nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="service_requests")
    task = relationship("Task", back_populates="request", uselist=False)
    rating = relationship("Rating", back_populates="request", uselist=False)
