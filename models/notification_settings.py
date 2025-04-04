from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func  # Для автоматического времени
from app_data.db_config import Base

class NotificationSettings(Base):
    __tablename__ = 'notification_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Исправлено на 'users.id'
    device_id = Column(Integer, ForeignKey('devices.id'))  # Исправлено на 'devices.id'
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    threshold = Column(Float)
    created_at = Column(DateTime, server_default=func.now())  # Добавлено время создания

    # Связи
    device = relationship("AquaState", back_populates="notifications")
    user = relationship("User")