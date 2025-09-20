import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Role(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    WORKER = "worker"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(Role), nullable=False)
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    service_requests = relationship("ServiceRequest", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    tasks = relationship("Task", back_populates="worker")
